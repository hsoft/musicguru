#import "cocoalib/Dialogs.h"
#import "cocoalib/ProgressController.h"
#import "cocoalib/Utils.h"
#import "AppDelegate.h"
#import "MassRenameDialog.h"
#import "SplitDialog.h"
#import "Consts.h"
#import "DesignWindow.h"

static NSString* tbbLocations   = @"tbbLocations";
static NSString* tbbDetails     = @"tbbDetails";
static NSString* tbbIgnoreBox   = @"tbbIgnoreBox";
static NSString* tbbAction      = @"tbbAction";
static NSString* tbbMaterialize = @"tbbMaterialize";

@implementation DesignOutlineView
- (NSColor *)determineDragCircleColor
{
    _alternateDragging = ([[NSApp currentEvent] modifierFlags] & NSCommandKeyMask) != 0;
    if (_alternateDragging)
        return [NSColor blueColor];
    else
        return [super determineDragCircleColor];
}

- (NSImage *)determineDragImage
{
    return [NSImage imageNamed:@"music_note_32"];
}

- (BOOL)performDragFrom:(DraggableOutlineView *)aSource withNodes:(NSArray *)aSourceNodes to:(OVNode *)aDestNode
{
    NSMutableArray *sourceNodePaths = [NSMutableArray array];
    NSEnumerator *e = [aSourceNodes objectEnumerator];
    OVNode *node;
    while (node = [e nextObject])
    {
        if ([(DesignOutlineView *)aSource alternateDragging])
        {
            //We must add *children* of dragged nodes
            int childCount = [[aSource dataSource] outlineView:aSource numberOfChildrenOfItem:node];
            for(int i=0;i<childCount;i++)
            {
                OVNode *snode = [[aSource dataSource] outlineView:aSource child:i ofItem:node];
                [sourceNodePaths addObject:p2a([snode indexPath])];
            }
        }
        else
            [sourceNodePaths addObject:p2a([node indexPath])];
    }
    if ((aDestNode) && (([[NSApp currentEvent] modifierFlags] & NSCommandKeyMask) != 0))
        aDestNode = [aDestNode parent];
    NSArray *destNodePath = [NSArray array];
    if (aDestNode)
        destNodePath = [Utils indexPath2Array:[aDestNode indexPath]];
    return n2b([(PyMusicGuru *)py performDragFrom:i2n([aSource tag]) withNodes:sourceNodePaths to:i2n([self tag]) withNode:destNodePath]);
}

- (BOOL)alternateDragging {return _alternateDragging;}
@end

@implementation DesignWindow
/* Initialize */
- (id)initWithParentApp:(id)aApp;
{
    self = [super initWithWindowNibName:@"Design"];
    [self window]; //Initialize widgets.
    AppDelegate *app = aApp;
    _app = app;
    _editedNode = nil;
    _editor = nil;
    _mediaCapacity = 0;
    py = [app py];
    _detailsPanel = [app detailsPanel];
    [browserOutline makeImagedColumnWithId:@"0"];
    [browserOutline setDoubleAction:@selector(renameClicked:)];
    [browserOutline setPy:py];
    [ignoreBoxOutline makeImagedColumnWithId:@"0"];
    [ignoreBoxOutline setPy:py];
    [self refreshStats];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(BoardLocationsChanged:) name:BoardLocationsChangedNotification object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(BoardLocationsChanged:) name:MPLChangedNotification object:nil];
    //Toolbar
    [[actionMenu itemAtIndex:0] setImage:[NSImage imageNamed: @"gear"]];
    NSToolbar *t = [[[NSToolbar alloc] initWithIdentifier:@"BuildWindowToolbar"] autorelease];
    [t setAllowsUserCustomization:NO];
    [t setAutosavesConfiguration:NO];
    [t setDisplayMode:NSToolbarDisplayModeIconAndLabel];
    [t setDelegate:self];
    [[self window] setToolbar:t];
    return self;
}
/* Private */
- (void)renameItemAtRow:(int)aRow
{
    OVNode *node = [browserOutline itemAtRow:aRow];
    if (!node)
        return;
    [browserOutline scrollRowToVisible:aRow];
    [browserOutline scrollColumnToVisible:0];
    int rowHeight = [browserOutline rowHeight];
    NSPoint origin = [browserOutline frame].origin;
    origin = [[[self window] contentView] convertPoint:origin fromView:browserOutline];
    origin.y = origin.y - 2 - ((rowHeight + 2) * (aRow + 1));
    NSTableColumn *firstColumn = [[browserOutline tableColumns] objectAtIndex:0];
    NSSize size = NSMakeSize([firstColumn width],rowHeight + 4);
    _editedNode = node;
    if (_editor)
    {
        [_editor removeFromSuperview];
        [_editor release];
    }
    _editor = [[NSTextField alloc] initWithFrame:NSMakeRect(origin.x,origin.y,size.width,size.height)];
    [_editor setFont:[[firstColumn dataCell] font]];
    NSString *nodeValue = [[browserOutline dataSource] outlineView:browserOutline objectValueForTableColumn:firstColumn byItem:node];
    [_editor setStringValue:nodeValue];
    [_editor setEditable:YES];
    [_editor setBordered:YES];
    [_editor setBezeled:YES];
    [_editor setDelegate:self];
    [[[self window] contentView] addSubview:_editor];
    [[self window] makeFirstResponder:_editor];
}

/* Action */
- (IBAction)massRename:(id)sender
{
    PyMassRenamePanel *panel = [py getMassRenamePanel];
    MassRenameDialog *dialog = [[[MassRenameDialog alloc] initWithPyMassRenamePanel:panel] autorelease];
    if ([dialog run])
    {
        [[ProgressController mainProgressController] setJobDesc:@"Renaming..."];
        [[ProgressController mainProgressController] setJobId:jobMassRename];
        [[ProgressController mainProgressController] showSheetForParent:[self window]];
        [py massRenameWithModel:[panel getModel] whitespaceType:[panel getWhitespace]];
    }
}

- (IBAction)materialize:(id)sender
{
    if (![_app canMaterialize])
        return;
    _wiz = [[MaterializeWizard alloc] initWithPy:py];
    [_wiz setMediaCapacity:_mediaCapacity];
    [_wiz runAsSessionWithCallback:@selector(materializeWizardCallback:) target:self];
}

- (IBAction)moveConflicts:(id)sender
{
    [py moveConflicts];
    [self refreshStats];
    [browserOutline reloadData];
    [ignoreBoxOutline reloadData];
    [ignoreBoxPanel orderFront:sender];
}

- (IBAction)moveConflictsAndOriginals:(id)sender
{
    [py moveConflictsAndOriginals];
    [self refreshStats];
    [browserOutline reloadData];
    [ignoreBoxOutline reloadData];
    [ignoreBoxPanel orderFront:sender];
}

- (IBAction)moveToIgnoreBox:(id)sender
{
    [py moveToIgnoreBox:[browserOutline selectedNodePaths]];
    [self refreshStats];
    [browserOutline selectRowIndexes:[NSIndexSet indexSet] byExtendingSelection:NO];
    [browserOutline reloadData];
    [ignoreBoxOutline reloadData];
    [ignoreBoxPanel orderFront:sender];
}

- (IBAction)newFolder:(id)sender
{
    OVNode *parentNode = nil;
    OVNode *selectedNode = [browserOutline itemAtRow:[browserOutline selectedRow]];
    if (selectedNode)
    {
        if ([py isNodeContainer:p2a([selectedNode indexPath])])
            parentNode = selectedNode;
        else
            parentNode = [selectedNode parent];
    }
    NSString *newFolderName;
    if (parentNode)
    {
        newFolderName = [py newFolderIn:p2a([parentNode indexPath])];
        [browserOutline reloadItem:parentNode reloadChildren:YES];
        [browserOutline expandItem:parentNode];
    }
    else
    {
        newFolderName = [py newFolderIn:nil];
        [browserOutline reloadData];
    }
    OVNode *newNode = [browserOutline findNodeWithName:newFolderName inParentNode:parentNode];
    int newNodeRow = [browserOutline rowForItem:newNode];
    [self renameItemAtRow:newNodeRow];
}

- (IBAction)removeEmptyFolders:(id)sender
{
    [py removeEmptyFolders];
    [browserOutline reloadData];
    [ignoreBoxOutline reloadData];
}

- (IBAction)renameClicked:(id)sender
{
    int clickedRow = [sender clickedRow];
    OVNode *node = [sender itemAtRow:clickedRow];
    if ((node) && ([sender clickedColumn] == 0))
        [self renameItemAtRow:clickedRow];
}

- (IBAction)renameSelected:(id)sender
{
    [self renameItemAtRow:[browserOutline selectedRow]];
}

- (IBAction)selectSong:(id)sender
{
    OutlineView *ov = sender;
    NSArray *nodePaths = [ov selectedNodePaths];
    [py selectBoardSongs:nodePaths];
    [_detailsPanel refresh];
}

- (IBAction)showIgnoreBox:(id)sender
{
    if ([ignoreBoxPanel isVisible])
        [ignoreBoxPanel close];
    else
        [ignoreBoxPanel orderFront:sender];
}

- (IBAction)split:(id)sender
{
    PySplitPanel *panel = [py getSplitPanel];
    SplitDialog *dialog = [[[SplitDialog alloc] initWithPySplitPanel:panel] autorelease];
    if ([dialog run])
    {
        _mediaCapacity = [[panel getCapacity] longLongValue];
        [[ProgressController mainProgressController] setJobDesc:@"Splitting..."];
        [[ProgressController mainProgressController] setJobId:jobSplit];
        [[ProgressController mainProgressController] showSheetForParent:[self window]];
        [py splitWithModel:[panel getModel] capacity:[panel getCapacity] groupingLevel:[panel getGroupingLevel]];
    }
}

- (IBAction)switchConflictAndOriginal:(id)sender
{
    NSArray *nodes = [browserOutline selectedNodes];
    if ([nodes count] != 1) //There must be exactly one selected node
        return;
    OVNode *node = [nodes objectAtIndex:0];
    [py switchConflictAndOriginal:p2a([node indexPath])];
    [self refreshStats];
    if ([node parent])
        [browserOutline reloadItem:[node parent] reloadChildren:YES];
    else
        [browserOutline reloadData];
}

- (IBAction)unsplit:(id)sender
{
    [py unsplit];
    [browserOutline reloadData];
}

//Public
- (void)materializeWizardCallback:(MaterializeWizard *)aWizard
{
    if ([_wiz collectionHasChanged])
    {
        [py emptyBoard];
        [[NSNotificationCenter defaultCenter] postNotificationName:MPLChangedNotification object:self];
        [[NSNotificationCenter defaultCenter] postNotificationName:BoardLocationsChangedNotification object:self];
    }
    [_wiz autorelease]; //autorelease: Let enough time to the wizard to finish it's operations if it has been cancelled in the middle of a getNextPage.
    _wiz = nil;
}

- (void)refresh
{
    [self refreshStats];
    [browserOutline reloadData];
    [ignoreBoxOutline reloadData];
}

- (void)refreshStats
{
    [statsLabel setStringValue:[py getBoardStats]];
}

- (void)setDetailsPanel:(DetailsPanel *)aDetailsPanel
{
    _detailsPanel = aDetailsPanel;
}

//Delegate
- (void)controlTextDidEndEditing:(NSNotification *)aNotification
{
    [[aNotification object] removeFromSuperview];
    NSString *oldName = [[_editedNode buffer] objectAtIndex:0];
    NSString *newName = [py renameNode:[Utils indexPath2Array:[_editedNode indexPath]] to:[[aNotification object] stringValue]];
    if (![newName isEqual:oldName])
    {
        if ([_editedNode parent])
            [browserOutline reloadItem:[_editedNode parent] reloadChildren:YES];
        else
            [browserOutline reloadData];
        _editedNode = [browserOutline findNodeWithName:newName inParentNode:[_editedNode parent]];
        [browserOutline selectRowIndexes:[NSIndexSet indexSetWithIndex:[browserOutline rowForItem:_editedNode]] byExtendingSelection:NO];
        [self refreshStats];
    }
    [[self window] makeFirstResponder:browserOutline];
}

-(void)outlineView:(DraggableOutlineView *)aDest draggedFrom:(DraggableOutlineView *)aSource
{
    [self refreshStats];
}

- (void)outlineView:(NSOutlineView *)outlineView willDisplayCell:(id)cell forTableColumn:(NSTableColumn *)tableColumn item:(id)item
{
    if ([[tableColumn identifier] isEqual:@"0"])
    {
        ArrowlessBrowserCell *c = cell;
        OVNode *node = item;
        NSString *imageName = [[node buffer] objectAtIndex:5]; //5 is the index for the image name value.
        [c setImage:[NSImage imageNamed:imageName]];
    }
}

- (void)windowDidResignKey:(NSNotification *)aNotification
{
    if (_editor)
    {
        [_editor removeFromSuperview];
        [_editor release];
        _editor = nil;
    }
}

/* Notifications */
- (void)BoardLocationsChanged:(NSNotification *)aNotification
{
    [self refreshStats];
    [browserOutline reloadData];
    [ignoreBoxOutline reloadData];
}

/* Toolbar */
- (NSToolbarItem *)toolbar:(NSToolbar *)toolbar itemForItemIdentifier:(NSString *)itemIdentifier willBeInsertedIntoToolbar:(BOOL)flag
{
    NSToolbarItem *tbi = [[[NSToolbarItem alloc] initWithItemIdentifier:itemIdentifier] autorelease];
    if (itemIdentifier == tbbLocations)
    {
        [tbi setLabel: @"Locations"];
        [tbi setToolTip: @"Show/Hide the locations drawer"];
        [tbi setImage: [NSImage imageNamed: @"locations_32"]];
        [tbi setTarget: _app];
        [tbi setAction: @selector(showLocations:)];
    }
    else if (itemIdentifier == tbbDetails)
    {
        [tbi setLabel: @"Details"];
        [tbi setToolTip: @"Show/Hide the details panel"];
        [tbi setImage: [NSImage imageNamed: @"info_32"]];
        [tbi setTarget: _app];
        [tbi setAction: @selector(showDetails:)];
    }
    else if (itemIdentifier == tbbIgnoreBox)
    {
        [tbi setLabel: @"Ignore Box"];
        [tbi setToolTip: @"Show/Hide the Ignore Box"];
        [tbi setImage: [NSImage imageNamed: @"ignore_box_32"]];
        [tbi setTarget: self];
        [tbi setAction: @selector(showIgnoreBox:)];
    }
    else if (itemIdentifier == tbbAction)
    {
        [tbi setLabel: @"Action"];
        [tbi setPaletteLabel: @"Action"];
        [tbi setView:actionMenuView];
        [tbi setMinSize:[actionMenuView frame].size];
        [tbi setMaxSize:[actionMenuView frame].size];
    }
    else if (itemIdentifier == tbbMaterialize)
    {
        [tbi setLabel: @"Materialize"];
        [tbi setToolTip: @"Apply changes you've made to your collection"];
        [tbi setImage: [NSImage imageNamed: @"materialize_32"]];
        [tbi setTarget: self];
        [tbi setAction: @selector(materialize:)];
    }
    [tbi setPaletteLabel: [tbi label]];
    return tbi;
}

- (NSArray *)toolbarAllowedItemIdentifiers:(NSToolbar *)toolbar
{
    return [NSArray arrayWithObjects:
        tbbLocations,
        tbbDetails,
        tbbIgnoreBox,
        tbbAction,
        tbbMaterialize,
        NSToolbarSeparatorItemIdentifier,
        NSToolbarSpaceItemIdentifier, 
        NSToolbarFlexibleSpaceItemIdentifier,
        nil];
}

- (NSArray *)toolbarDefaultItemIdentifiers:(NSToolbar *)toolbar
{
    return [NSArray arrayWithObjects:
        tbbLocations,
        tbbDetails,
        tbbIgnoreBox,
        NSToolbarSpaceItemIdentifier,
        tbbAction,
        NSToolbarSpaceItemIdentifier,
        tbbMaterialize,
        nil];
}

- (BOOL)validateToolbarItem:(NSToolbarItem *)aItem
{
    return [self validateAction:[aItem action] fromToolbar:YES];
}

- (BOOL)validateMenuItem:(id <NSMenuItem>)aMenuItem
{
    return [self validateAction:[aMenuItem action] fromToolbar:NO];
}

- (BOOL)validateAction:(SEL)aAction fromToolbar:(BOOL)aFromToolbar
{
    BOOL r = YES;
    if (
        (aAction == @selector(massRename:)) ||
        (aAction == @selector(split:)) ||
        (aAction == @selector(materialize:)) ||
        (aAction == @selector(newFolder:)) ||
        (aAction == @selector(renameSelected:)) ||
        (aAction == @selector(moveToIgnoreBox:)) ||
        (aAction == @selector(removeEmptyFolders:)) ||
        (aAction == @selector(moveConflicts:)) ||
        (aAction == @selector(moveConflictsAndOriginals:)) ||
        (aAction == @selector(switchConflictAndOriginal:)) ||
        (aAction == @selector(materialize:))
    )
        r = [browserOutline numberOfRows] > 0;
    if (r && ((aAction == @selector(moveConflicts:)) || (aAction == @selector(moveConflictsAndOriginals:))))
        r = [py conflictCount] > 0;
    if (r && ((aAction == @selector(renameSelected:)) || (aAction == @selector(moveToIgnoreBox:))))
        r = [[browserOutline selectedRowIndexes] count] > 0;
    if (r && (aAction == @selector(switchConflictAndOriginal:)))
    {
        NSArray *nodes = [browserOutline selectedNodes];
        if ([nodes count] == 1)
            r = n2b([py isNodeConflicted:p2a([[nodes objectAtIndex:0] indexPath])]);
        else
            r = NO;
    }
    if (r && (aAction == @selector(split:)))
        r = !n2b([py isBoardSplitted]);
    if (r && (aAction == @selector(unsplit:)))
        r = n2b([py isBoardSplitted]);
    return r;
}

@end
