#import <Cocoa/Cocoa.h>
#import "Wizard.h"
#import <cocoalib/Table.h>

@interface RecordingOptionsPage : WizPage
{
    IBOutlet NSButton *addRecordedSwitch;
    IBOutlet TableView *cdTable;
}
@end
