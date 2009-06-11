#import "AddLocationWindow.h"
#import "cocoalib/Dialogs.h"

@implementation AddLocationWindow

- (id)initWithDelegate:(id)aDelegate
{
    self = [super initWithWindowNibName:@"AddLocation"];
    [self setCurrentPath:@""];
    _delegate = aDelegate;
    _mediaList = [[[NSWorkspace sharedWorkspace] mountedRemovableMedia] retain];
    NSNotificationCenter *nc = [[NSWorkspace sharedWorkspace] notificationCenter];
    [nc addObserver:self selector:@selector(onMountOrUnmount:) name:NSWorkspaceDidMountNotification object:nil];
    [nc addObserver:self selector:@selector(onMountOrUnmount:) name:NSWorkspaceDidUnmountNotification object:nil];
    [self window]; // Create the window so locationTypeChange works.
    [self locationTypeChange:self];
    return self;
}

- (void)dealloc
{
    [[[NSWorkspace sharedWorkspace] notificationCenter] removeObserver:self];
    [super dealloc];
}

- (IBAction)addLocation:(id)sender
{
    [[self window] close];
    if ([_delegate respondsToSelector:@selector(addLocationWithPath:name:removeable:)])
    {
        BOOL bRemoveable = ([locationTypeSelector selectedRow] == 2);
        NSString *r = [_delegate addLocationWithPath:[self currentPath] name:[locationNameText stringValue] removeable:bRemoveable];
        if ((r) && ([r length]))
        {
            [Dialogs showMessage:r];
            [self showWindow:self];
            return;
        }
    }
}

- (IBAction)choosePath:(id)sender
{
    NSOpenPanel *op = [NSOpenPanel openPanel];
    [op setCanChooseFiles:NO];
    [op setCanChooseDirectories:YES];
    if ([op runModalForTypes:nil] == NSOKButton)
    {
        [locationPathText setStringValue:[[op filenames] objectAtIndex:0]];
        [self controlTextDidChange:nil];
    }
}

- (IBAction)locationTypeChange:(id)sender
{
    switch ([locationTypeSelector selectedRow])
    {
        case 0:
        {
            [itunesBox setHidden:NO];
            [fixedBox setHidden:YES];
            [removeableBox setHidden:YES];
            [self setCurrentPath:[@"~/Music/iTunes/iTunes Music" stringByExpandingTildeInPath]];
            [locationNameText setStringValue:@"iTunes"];
            break;
        }
        case 1:
        {
            [itunesBox setHidden:YES];
            [fixedBox setHidden:NO];
            [removeableBox setHidden:YES];
            [self controlTextDidChange:nil];
            break;
        }
        case 2:
        {
            [itunesBox setHidden:YES];
            [fixedBox setHidden:YES];
            [removeableBox setHidden:NO];
            [self tableViewSelectionDidChange:nil];
            break;
        }
    }
}

//Private
- (NSString *)locationNameFromPath:(NSString *)aPath
{
    if ([aPath length])
        return [[aPath pathComponents] lastObject];
    else
        return @"";
}

- (void)onMountOrUnmount:(NSNotification *)notification
{
    [_mediaList release];
    _mediaList = [[[NSWorkspace sharedWorkspace] mountedRemovableMedia] retain];
    [removeableMediaTable reloadData];
    [self tableViewSelectionDidChange:nil];
}

//Data Source
- (int)numberOfRowsInTableView:(NSTableView *)aTableView
{
    return [_mediaList count];
}

- (id)tableView:(NSTableView *)aTableView objectValueForTableColumn:(NSTableColumn *)aTableColumn row:(int)rowIndex
{
    return [self locationNameFromPath:[_mediaList objectAtIndex:rowIndex]];
}

//Delegate
- (void)tableViewSelectionDidChange:(NSNotification *)aNotification
{
    if ([locationTypeSelector selectedRow] != 2)
        return;
    if ([removeableMediaTable selectedRow] >= 0)
        [self setCurrentPath:[_mediaList objectAtIndex:[removeableMediaTable selectedRow]]];
    else
        [self setCurrentPath:@""];
    [locationNameText setStringValue:[self locationNameFromPath:[self currentPath]]];
}

- (void)controlTextDidChange:(NSNotification *)aNotification
{
    [self setCurrentPath:[locationPathText stringValue]];
    [locationNameText setStringValue:[self locationNameFromPath:[self currentPath]]];
}

//Properties
- (NSString *)currentPath {return _currentPath;}
- (void)setCurrentPath:(NSString *)aPath
{
    [_currentPath release];
    _currentPath = [aPath retain];
}
@end
