/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "DiskNeededPanel.h"

@implementation DiskNeededPanel
+ (NSString *)promptForDiskNamed:(NSString *)aDiskName
{
    DiskNeededPanel *dnp = [[DiskNeededPanel alloc] init];
    NSString *r = [dnp promptForDiskNamed:aDiskName];
    [dnp release];
    return r;
}

- (id)init
{
    self = [super initWithWindowNibName:@"DiskNeeded"];
    [self window]; //Initialize widgets
    return self;
}

- (IBAction)cancel:(id)sender
{
    [NSApp stopModalWithCode:NSCancelButton];
}

- (IBAction)ejectSelected:(id)sender
{
    NSString *pathToEject = [_mediaList objectAtIndex:[volumeTable selectedRow]];
    [[NSWorkspace sharedWorkspace] unmountAndEjectDeviceAtPath:pathToEject];
    [self onMountOrUnmount:nil];
}

- (IBAction)ok:(id)sender
{
    [NSApp stopModalWithCode:NSOKButton];
}

- (NSString *)promptForDiskNamed:(NSString *)aDiskName
{
    _mediaList = [[[NSWorkspace sharedWorkspace] mountedRemovableMedia] retain];
    NSNotificationCenter *nc = [[NSWorkspace sharedWorkspace] notificationCenter];
    [nc addObserver:self selector:@selector(onMountOrUnmount:) name:NSWorkspaceDidMountNotification object:nil];
    [nc addObserver:self selector:@selector(onMountOrUnmount:) name:NSWorkspaceDidUnmountNotification object:nil];
    [self onMountOrUnmount:nil];
    [messageLabel setStringValue:[NSString stringWithFormat:@"Insert the CD labeled '%@'.",aDiskName]];
    _running = YES;
    [NSThread detachNewThreadSelector:@selector(threadedMountCheck) toTarget:self withObject:nil];
    NSString *r = @"";
    if ([NSApp runModalForWindow:[self window]] == NSOKButton)
        r = [_mediaList objectAtIndex:[volumeTable selectedRow]];
    _running = NO;
    [[self window] close];
    return r;
}

- (void)threadedMountCheck
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    while (_running)
    {
        [self onMountOrUnmount:nil];
        [NSThread sleepUntilDate:[[NSDate date] addTimeInterval:1]];
    }
    [pool release];
}

- (void)windowWillClose:(NSNotification *)aNotification
{
    [[[NSWorkspace sharedWorkspace] notificationCenter] removeObserver:self];
    if ([NSApp modalWindow])
        [NSApp stopModalWithCode:NSCancelButton];
}

//Data Source
- (NSInteger)numberOfRowsInTableView:(NSTableView *)aTableView
{
    return [_mediaList count];
}

- (id)tableView:(NSTableView *)aTableView objectValueForTableColumn:(NSTableColumn *)aTableColumn row:(NSInteger)rowIndex
{
    return [[[_mediaList objectAtIndex:rowIndex] pathComponents] lastObject];
}

//Delegate
- (void)onMountOrUnmount:(NSNotification *)notification
{
    [_mediaList release];
    _mediaList = [[[NSWorkspace sharedWorkspace] mountedRemovableMedia] retain];
    [volumeTable reloadData];
    [okButton setEnabled:[_mediaList count]];
}
@end
