/* SplittingOptionsDialog */

#import <Cocoa/Cocoa.h>
#import "PyMusicGuru.h"

@interface SplitDialog : NSWindowController
{
    IBOutlet NSMatrix *capacitySelector;
    IBOutlet NSTextField *customCapacityText;
    IBOutlet NSTextField *customModelText;
    IBOutlet NSTextField *groupingExampleLabel;
    IBOutlet NSSlider *groupingSlider;
    IBOutlet NSMatrix *modelSelector;
    
    PySplitPanel *py;
}
- (id)initWithPySplitPanel:(PySplitPanel *)aPy;
- (void)dealloc;

- (IBAction)cancel:(id)sender;
- (IBAction)changeExample:(id)sender;
- (IBAction)ok:(id)sender;

- (BOOL)run;
@end
