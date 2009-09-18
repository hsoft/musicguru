/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "SplitDialog.h"
#import "cocoalib/Utils.h"

@implementation SplitDialog
- (id)initWithPySplitPanel:(PySplitPanel *)aPy
{
    self = [super initWithWindowNibName:@"Split"];
    py = [aPy retain];
    [self window]; //Initialize Widgets
    return self;
}

- (void)dealloc
{
    [py release];
    [super dealloc];
}

- (IBAction)cancel:(id)sender
{
    [NSApp stopModalWithCode:NSCancelButton];
    [[self window] close];
}

- (IBAction)changeExample:(id)sender
{
    [py setGroupingLevel:i2n([groupingSlider intValue])];
    [groupingExampleLabel setStringValue:[py getGroupingExample]];
}

- (IBAction)ok:(id)sender
{
    [NSApp stopModalWithCode:NSOKButton];
    [[self window] close];
}

- (BOOL)run
{
    //Returns YES if OK was clicked, and NO otherwise.
    [self changeExample:self];
    if ([NSApp runModalForWindow:[self window]] == NSOKButton)
    {
        [py setModelSelectedRow:i2n([modelSelector selectedRow])];
        [py setCapacitySelectedRow:i2n([capacitySelector selectedRow])];
        int customCapacity = [customCapacityText intValue];
        if (customCapacity)
            [py setCustomCapacity:i2n(customCapacity)];
        [py setCustomModel:[customModelText stringValue]];
        return YES;
    }
    else
        return NO;
}

@end
