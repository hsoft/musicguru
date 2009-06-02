#import "FreeSpacePage.h"
#import <cocoalib/Utils.h>

@implementation FreeSpacePage
- (id)init
{
    self = [super init];
    [self setTitle:@"Free Disk Space"];
    return self;
}

- (void)loadInfo:(NSMutableDictionary *)aInfo
{
    py = [aInfo objectForKey:@"py"];
    [self evaluateFreeSpace];
}

- (void)saveInfo:(NSMutableDictionary *)aInfo
{
    if (![self evaluateFreeSpace])
        @throw @"You don't have enough free space to continue. Free some disk space and try again.";
}

- (IBAction)evaluateFreeSpace:(id)sender
{
    [self evaluateFreeSpace];
}

- (BOOL)evaluateFreeSpace
{
    NSArray *sizes = [py getBurnBufferSizes];
    long long freeBytes = [[sizes objectAtIndex:0] longLongValue];
    long long minimumBytes = [[sizes objectAtIndex:1] longLongValue];
    long long recommendedBytes = [[sizes objectAtIndex:2] longLongValue];
    if (freeBytes < minimumBytes)
    {
        [messageLabel setStringValue:@"You do NOT have enough free disk space."];
        [freeSpaceImage setImage:[NSImage imageNamed:@"red"]];
    }
    else if (freeBytes < recommendedBytes)
    {
        [messageLabel setStringValue:@"You have enough disk space, but could use more."];
        [freeSpaceImage setImage:[NSImage imageNamed:@"yellow"]];
    }
    else
    {
        [messageLabel setStringValue:@"You have enough disk space."];
        [freeSpaceImage setImage:[NSImage imageNamed:@"green"]];
    }
    [freeSpaceLabel setStringValue:[sizes objectAtIndex:3]];
    [minimumLabel setStringValue:[sizes objectAtIndex:4]];
    [recommendedLabel setStringValue:[sizes objectAtIndex:5]];
    return freeBytes >= minimumBytes;
}

@end
