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
