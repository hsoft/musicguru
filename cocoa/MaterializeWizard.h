#import <Cocoa/Cocoa.h>
#import "WizCommonPages.h"
#import "PyMusicGuru.h"
#import "FreeSpacePage.h"
#import "InsertBlankDiskPage.h"
#import "MaterializeChoicePage.h"
#import "PathChoicePage.h"
#import "RecordingOptionsPage.h"
#import "RegistrationRequiredPage.h"

@interface MaterializeWizard : NSObject
{
    IBOutlet FreeSpacePage *freeSpacePage;
    IBOutlet InsertBlankDiskPage *insertBlankDiskPage;
    IBOutlet MaterializeChoicePage *materializeChoicePage;
    IBOutlet PathChoicePage *pathChoicePage;
    IBOutlet RecordingOptionsPage *recordingOptionsPage;
    IBOutlet RegistrationRequiredPage *registrationRequiredPage;
    
    SEL _callback;
    BOOL _collectionHasChanged; //This flag goes to YES when a RenameInRespectiveLocations or MoveFiles happen.
    WizCommonPages *_common;
    BOOL _firstCD;
    id _target;
    Wizard *_wizard;
}
- (id)initWithPy:(PyMusicGuru *)aPy;
- (void)dealloc;

- (NSString *)promptForDiskNamed:(NSString *)aDiskName;
- (BOOL)run;
- (void)runAsSessionWithCallback:(SEL)aCallback target:(id)aTarget;
- (WizPage *)wizardNeedsNextPage:(Wizard *)aWizard;

- (BOOL)collectionHasChanged;
- (void)setMediaCapacity:(long long)aCapacity;
@end
