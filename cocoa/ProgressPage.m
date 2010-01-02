/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "ProgressPage.h"

@implementation ProgressPage
- (void)setJobDesc:(NSString *)desc
{
    [messageLabel setStringValue:desc];
    [self processAppEvents];
}

- (BOOL)update:(int)newProgress
{
    [progress setIndeterminate:NO];
    [progress setDoubleValue:newProgress];
    [self processAppEvents];
    return [[self page] superview] != nil;
}

- (NSNumber *)pyUpdate:(NSNumber *)newProgress
{
    return [NSNumber numberWithBool:[self update:[newProgress intValue]]];
}

- (void)processAppEvents
{
    NSEvent *e = [NSApp nextEventMatchingMask:NSAnyEventMask untilDate:nil inMode:NSDefaultRunLoopMode dequeue:YES];
    while (e != nil)
    {
        [NSApp sendEvent:e];
        e = [NSApp nextEventMatchingMask:NSAnyEventMask untilDate:nil inMode:NSDefaultRunLoopMode dequeue:YES];
    }
}
@end
