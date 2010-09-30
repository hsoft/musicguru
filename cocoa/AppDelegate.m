/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "AppDelegate.h"
#import "ProgressController.h"
#import "HSFairwareReminder.h"
#import "Dialogs.h"
#import "Utils.h"
#import "Consts.h"

@implementation AppDelegate
+ (void)initialize
{
    NSUserDefaults *ud = [NSUserDefaults standardUserDefaults];
    NSMutableDictionary *d = [NSMutableDictionary dictionaryWithCapacity:10];
    [d setObject:@"%group:artist:emp:upper%/%artist%/%track% - %artist% - %title%" forKey:@"CustomModel"];
    [[NSUserDefaultsController sharedUserDefaultsController] setInitialValues:d];
    [ud registerDefaults:d];
}

- (void)awakeFromNib
{
    _detailsPanel = [[DetailsPanel alloc] initWithPy:py];
    _locationPanel = [[LocationPanel alloc] initWithPy:py];
    _designWindow = [[DesignWindow alloc] initWithParentApp:self];
    [[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(jobCompleted:) name:JobCompletedNotification object:nil];
    [self showDesignBoard:self];
    [self showLocations:self];
}
/* Actions */
- (IBAction)addLocation:(id)sender
{
    [self showLocations:sender];
    [_locationPanel addLocation:sender];
}
- (IBAction)openWebsite:(id)sender
{
    [[NSWorkspace sharedWorkspace] openURL:[NSURL URLWithString:@"http://www.hardcoded.net"]];
}

- (IBAction)redirectToBoard:(id)sender
{
    SEL action = [self getBoardActionForTag:[sender tag]];
    [NSApp sendAction:action to:_designWindow from:sender];
}

- (IBAction)removeLocation:(id)sender
{
    [self showLocations:sender];
    [_locationPanel removeLocation:sender];
}

- (IBAction)showDesignBoard:(id)sender
{
    [_designWindow showWindow:self];
}

- (IBAction)showDetails:(id)sender
{
    if ([[_detailsPanel window] isVisible])
        [[_detailsPanel window] close];
    else
        [[_detailsPanel window] orderFront:self];
}

- (IBAction)showIgnoreBox:(id)sender
{
    [self showDesignBoard:sender];
    [_designWindow showIgnoreBox:sender];
}

- (IBAction)showLocations:(id)sender
{
    [_locationPanel showWindow:self];
}

- (IBAction)updateCollection:(id)sender
{
    [self showLocations:sender];
    [_locationPanel updateCollection:sender];
}

/* Public */
- (BOOL)canMaterialize
{
    return [_locationPanel canMaterialize];
}

- (SEL)getBoardActionForTag:(int)aTag
{
    if (aTag == 0)
        return @selector(newFolder:);
    else if (aTag == 1)
        return @selector(removeEmptyFolders:);
    else if (aTag == 2)
        return @selector(renameSelected:);
    else if (aTag == 3)
        return @selector(moveToIgnoreBox:);
    else if (aTag == 4)  
        return @selector(switchConflictAndOriginal:);
    else if (aTag == 5)
        return @selector(massRename:);
    else if (aTag == 6)
        return @selector(split:);
    else if (aTag == 7)
        return @selector(unsplit:);
    else if (aTag == 8)
        return @selector(moveConflicts:);
    else if (aTag == 9)
        return @selector(moveConflictsAndOriginals:);
    else if (aTag == 10)
        return @selector(materializeInPlace:);
    else if (aTag == 11)
        return @selector(copyToLocation:);
    else if (aTag == 12)
        return @selector(moveToLocation:);
    return nil;
}

/* Properties */
- (DetailsPanel *)detailsPanel {return _detailsPanel;}
- (PyMusicGuru *)py {return py;}

/* Notification */
- (void)applicationDidBecomeActive:(NSNotification *)aNotification
{
    if (![[_designWindow window] isVisible])
        [self showDesignBoard:self];
}

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification
{
    [HSFairwareReminder showNagWithApp:py];
    [[ProgressController mainProgressController] setWorker:py];
    [self updateCollection:self];
}

- (void)applicationWillTerminate:(NSNotification *)aNotification
{
    for (int i=0;i<[[NSApp windows] count];i++)
        [[[NSApp windows] objectAtIndex:i] close];
}

- (void)jobCompleted:(NSNotification *)aNotification
{
    NSString *jobId = [[ProgressController mainProgressController] jobId];
    if ((jobId == jobUpdate) || (jobId == jobAddLocation))
    {
        [[NSNotificationCenter defaultCenter] postNotificationName:MPLChangedNotification object:self];
    }
    else if ((jobId == jobMassRename) || (jobId == jobSplit))
    {
        [_designWindow refresh];
    }
    else if ((jobId == jobMaterializeInPlace) || (jobId == jobMaterializeMove)) {
        [py emptyBoard];
        [[NSNotificationCenter defaultCenter] postNotificationName:MPLChangedNotification object:self];
        [[NSNotificationCenter defaultCenter] postNotificationName:BoardLocationsChangedNotification object:self];
    }
}

/* Delegate */
- (NSApplicationTerminateReply)applicationShouldTerminate:(NSApplication *)sender
{
    if ([[py getOutlineView:0 childCountsForPath:[NSArray array]] count] > 0)
    {
        if ([Dialogs askYesNo:@"The Design Board is not empty. Are you sure you want to quit?"] == NSAlertSecondButtonReturn)
            return NSTerminateCancel;
    }
    return NSTerminateNow;
}

- (BOOL)validateMenuItem:(NSMenuItem *)aMenuItem
{
    SEL action = [aMenuItem action];
    if (action == @selector(redirectToBoard:))
    {
        SEL action = [self getBoardActionForTag:[aMenuItem tag]];
        return [_designWindow validateAction:action fromToolbar:NO];
    }
    return YES;
}
@end
