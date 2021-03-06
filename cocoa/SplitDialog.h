/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

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
