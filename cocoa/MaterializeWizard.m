#import "MaterializeWizard.h"
#import "cocoalib/Dialogs.h"
#import "cocoalib/Utils.h"
#import "cocoalib/RegistrationInterface.h"
#import "DiskNeededPanel.h"
#import "Consts.h"

@implementation MaterializeWizard
- (id)initWithPy:(PyMusicGuru *)aPy
{
    self = [super init];
    [NSBundle loadNibNamed:@"WizMaterialize" owner:self];
    _wizard = [[Wizard alloc] initWithDelegate:self];
    [_wizard setImage:[NSImage imageNamed:@"materialize_48"]];
    [[_wizard window] setTitle:@"Materialize Wizard"];
    [[_wizard info] setObject:aPy forKey:@"py"];
    _common = [[WizCommonPages alloc] init];
    _collectionHasChanged = NO;
    _firstCD = YES;
    return self;
}

- (void)dealloc
{
    [_common release];
    [_wizard release];
    [super dealloc];
}

- (NSString *)promptForDiskNamed:(NSString *)aDiskName
{
    NSString *r = [DiskNeededPanel promptForDiskNamed:aDiskName];
    if ([r length])
        return r;
    else
    {
        if ([_wizard windowShouldClose:self])
        {
            [_wizard stopModalWithCode:NSCancelButton];
            return nil;
        }
        else
            return [self promptForDiskNamed:aDiskName];
    }
}

- (BOOL)run
{
    return [_wizard run];
}

- (void)runAsSessionWithCallback:(SEL)aCallback target:(id)aTarget
{
    _callback = aCallback;
    _target = aTarget;
    [_wizard runAsSession];
}

- (void)wizard:(Wizard *)aWizard ModalSessionEndedWithCode:(int)aCode
{
    [NSApp sendAction:_callback to:_target from:self];
}

- (WizPage *)wizardNeedsNextPage:(Wizard *)aWizard
{
    if (![aWizard currentPage])
        return materializeChoicePage;
    PyMusicGuru *py = [[aWizard info] objectForKey:@"py"];
    int materializeType = n2i([[aWizard info] objectForKey:@"MaterializeType"]);
    if (materializeType == 0)
    {
        if (![py isRegistered])
            return registrationRequiredPage;
        if (([aWizard currentPage] == materializeChoicePage) || ([aWizard currentPage] == registrationRequiredPage))
        {
            [aWizard blockPrevious];
            _collectionHasChanged = YES;
            [py setProgressController:[_common progressPage]];
            [[_common progressPage] setTitle:@"Renaming files"];
            [aWizard startNonInteractiveSessionWithPage:[_common progressPage]];
            [py renameInRespectiveLocations];
            [py setProgressController:nil];
            [aWizard stopNonInteractiveSession];
        }
    }
    if ((materializeType == 1) || (materializeType == 2))
    {
        if ([aWizard currentPage] == materializeChoicePage)
            return pathChoicePage;
        if (![py isRegistered])
            return registrationRequiredPage;
        if (([aWizard currentPage] == pathChoicePage) || ([aWizard currentPage] == registrationRequiredPage))
        {
            [aWizard blockPrevious];
            if (materializeType == 1)
            {
                [[_common progressPage] setTitle:@"Moving files"];
                _collectionHasChanged = YES;
            }
            else
                [[_common progressPage] setTitle:@"Copying files"];
            [py setProgressController:[_common progressPage]];
            [aWizard startNonInteractiveSessionWithPage:[_common progressPage]];
            [py copyOrMove:b2n((materializeType == 2)) toPath:[[aWizard info] objectForKey:@"ChosenPath"] onNeedCDPanel:self];
            [py setProgressController:nil];
            [aWizard stopNonInteractiveSession];
        }
    }
    if (materializeType == 3)
    {
        if ([aWizard currentPage] == materializeChoicePage)
            return recordingOptionsPage;
        if ([aWizard currentPage] == recordingOptionsPage)
        {
            if (n2b([py prepareBurning]))
                return freeSpacePage;
        }
        if (![py isRegistered])
            return registrationRequiredPage;
        [aWizard blockPrevious];
        if ((!_firstCD) && ([aWizard currentPage] != insertBlankDiskPage))
        {
            // Finish the previous CD and prepare next.
            if (n2b([[aWizard info] objectForKey:@"AddRecorded"]))
            {
                if (!n2b([py addCurrentDiskToMPLOverwrite:b2n(NO)]))
                {
                    if ([Dialogs askYesNo:[NSString stringWithFormat:@"The disk '%@' already exists in your collection, do you want to overwrite it?",[py getDestinationDiskName]]] == NSAlertFirstButtonReturn)
                        [py addCurrentDiskToMPLOverwrite:b2n(YES)];
                }
                [[NSNotificationCenter defaultCenter] postNotificationName:MPLChangedNotification object:self];
            }
            [py cleanBuffer];
            [py prepareNextCDToBurn];
        }
        if (!n2b([py isFinishedBurning]))
        {
            if ([aWizard currentPage] != insertBlankDiskPage)
            {
                //Fetch source songs
                [[_common progressPage] setTitle:@"Fetching Songs"];
                [py setProgressController:[_common progressPage]];
                [aWizard startNonInteractiveSessionWithPage:[_common progressPage]];
                [py fetchSourceSongsWithNeedCDPanel:self];
                [py setProgressController:nil];
                [aWizard stopNonInteractiveSession];
                return insertBlankDiskPage;
            }
            else
            {
                //Burn fetched
                [py burnCurrentDiskWithWindow:[aWizard window]];
                _firstCD = NO;
                [[_common messagePage] setTitle:@"Recording..."];
                [[_common messagePage] setMessage:[NSString stringWithFormat:@"The disc '%@' is currently being recorded. When the disc is finished being recorded (And when you're finished writing the name of the CD on it.), click Next to continue.",[py getDestinationDiskName]]];
                return [_common messagePage];
            }
        }
    }
    [aWizard setCurrentPageAsLast];
    [[_common messagePage] setTitle:@"Finished"];
    [[_common messagePage] setMessage:@"The materialize operation is now finished. Click on 'Finish' to close this wizard."];
    return [_common messagePage];
}

- (BOOL)collectionHasChanged {return _collectionHasChanged;}

- (void)setMediaCapacity:(long long)aCapacity
{
    [[_wizard info] setObject:[NSNumber numberWithLongLong:aCapacity] forKey:@"MediaCapacity"];
}
@end
