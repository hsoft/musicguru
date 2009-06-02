#import "LocationPanel.h"
#import "Consts.h"
#import <cocoalib/Dialogs.h>
#import <cocoalib/ProgressController.h>
#import <cocoalib/Utils.h>

@implementation LocationPanel
- (id)initWithPy:(PyApp *)aPy
{
    self = [super initWithWindowNibName:@"LocationPanel"];
    [self window]; //So the locationsTable is initialized.
    _addLocation = nil;
    py = (PyMusicGuru *)aPy;
    [locationsTable setPy:aPy];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(MPLChanged:) name:MPLChangedNotification object:nil];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(locationTableSelectionChanged:) name:NSTableViewSelectionDidChangeNotification object:locationsTable];
    // Force the first locationTableSelectionChanged: so we can populate the details with initial values
    [self updateLocationDetails];
    return self;
}

// Verifies if all checked locations (except removable ones) are available
- (BOOL)canMaterialize
{
    [locationsTable reloadData];
    NSIndexSet *marked = [locationsTable markedIndexes];
    for (int i=0; i<[locationsTable numberOfRows]; i++)
    {
        if ([marked containsIndex:i])
        {
            BOOL isRemovable = n2b([locationsTable bufferValueForRow:i column:3]);
            BOOL isAvailable = n2b([locationsTable bufferValueForRow:i column:4]);
            if ((!isRemovable) && (!isAvailable))
            {
                NSString *name = [locationsTable bufferValueForRow:i column:0];
                NSString *path = [locationsTable bufferValueForRow:i column:5];
                NSString *message = [NSString stringWithFormat:@"The location '%@' at path '%@' is unreachable. You can't materialize your design.",name,path];
                [Dialogs showMessage:message];
                return NO;
            }
        }
    }
    return YES;
}

- (void)updateLocationDetails
{
    int i = [locationsTable selectedRow];
    NSString *path = @"";
    NSString *type = @"";
    BOOL canChangePath = NO;
    if (i >= 0)
    {
        BOOL isRemovable = n2b([locationsTable bufferValueForRow:i column:3]);
        path = [locationsTable bufferValueForRow:i column:5];
        type = isRemovable ? @"Removable (CD/DVD)" : @"Fixed (Hard disk)";
        canChangePath = !isRemovable;
    }
    [pathLabel setStringValue: [NSString stringWithFormat:@"Path: %@",path]];
    [typeLabel setStringValue: [NSString stringWithFormat:@"Type: %@",type]];
    [changeLocationPathButton setEnabled:canChangePath];
}

- (IBAction)addLocation:(id)sender
{
    if (_addLocation == nil)
        _addLocation = [[AddLocationWindow alloc] initWithDelegate:self];
    [_addLocation showWindow:self];
}

- (IBAction)changeLocationPath:(id)sender;
{
    int i = [locationsTable selectedRow];
    if (i < 0)
        return;
    NSOpenPanel *op = [NSOpenPanel openPanel];
    [op setCanChooseFiles:NO];
    [op setCanChooseDirectories:YES];
    if ([op runModalForTypes:nil] == NSOKButton)
    {
        NSString *name = [locationsTable bufferValueForRow:i column:0];
        NSString *newPath = [[op filenames] objectAtIndex:0];
        [py setPath:newPath ofLocationNamed:name];
        [self updateLocationDetails];
        [[ProgressController mainProgressController] setJobDesc:@"Updating Location..."];
        [[ProgressController mainProgressController] setJobId:jobUpdate];
        [[ProgressController mainProgressController] showSheetForParent:[self window]];
        [py updateLocationNamed:name];
    }
}

- (IBAction)markLocation:(id)sender
{
     if ([[py isBoardSplitted] boolValue])
     {
         [Dialogs showMessage:@"You cannot add or remove locations to a splitted design board. Unsplit it before adding or removing locations."];
         return;
     }
     [py toggleLocation:i2n([locationsTable clickedRow])];
     [locationsTable setMarkedIndexes:nil]; //Reset markings.
     [[NSNotificationCenter defaultCenter] postNotificationName:BoardLocationsChangedNotification object:self];
}

- (IBAction)removeLocation:(id)sender
{
    int i = [locationsTable selectedRow];
    if (i < 0)
        return;
    NSString *s = [[py getTableView:i2n(0) valuesForRow:i2n(i)] objectAtIndex:0];
    if ([Dialogs askYesNo:[NSString stringWithFormat:@"Do you really want to remove location '%@' from your collection?",s]] == NSAlertFirstButtonReturn)
    {
        [py removeLocationNamed:s];
        [[NSNotificationCenter defaultCenter] postNotificationName:MPLChangedNotification object:self];
    }
}

- (IBAction)updateCollection:(id)sender;
{
    [[ProgressController mainProgressController] setJobDesc:@"Updating Collection..."];
    [[ProgressController mainProgressController] setJobId:jobUpdate];
    [[ProgressController mainProgressController] showSheetForParent:[self window]];
    [py updateCollection];
}

//Delegate
- (NSString *)addLocationWithPath:(NSString *)aPath name:(NSString *)aName removeable:(BOOL)aRemoveable
{
    NSString *r = [py canAddLocationWithPath:aPath name:aName];
    if (r && [r length])
        return r;
    [[ProgressController mainProgressController] setJobDesc:@"Adding Location..."];
    [[ProgressController mainProgressController] setJobId:jobAddLocation];
    [[ProgressController mainProgressController] showSheetForParent:[self window]];
    [py addLocationWithPath:aPath name:aName removeable:[NSNumber numberWithBool:aRemoveable]];
    return @"";
}

- (void)tableView:(NSTableView *)aTableView willDisplayCell:(id)cell forTableColumn:(NSTableColumn *)aTableColumn row:(int)rowIndex
{
    BOOL isRemovable = n2b([locationsTable bufferValueForRow:rowIndex column:3]);
    BOOL isAvailable = n2b([locationsTable bufferValueForRow:rowIndex column:4]);
    if ([cell isKindOfClass:[NSTextFieldCell class]])
    {
        // Determine if the text color will be blue due to directory being reference.
        NSTextFieldCell *textCell = cell;
        if (isRemovable)
            [textCell setTextColor:[NSColor blueColor]];
        else if (!isAvailable)
            [textCell setTextColor:[NSColor redColor]];
        else
            [textCell setTextColor:[NSColor blackColor]];
    }
}

/* Notifications */
- (void)locationTableSelectionChanged:(NSNotification *)aNotification
{
    [self updateLocationDetails];
}

- (void)MPLChanged:(NSNotification *)aNotification
{
    [locationsTable reloadData];
    [self updateLocationDetails];
}
@end
