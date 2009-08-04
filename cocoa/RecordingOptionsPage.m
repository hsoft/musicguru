/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "RecordingOptionsPage.h"
#import "PyMusicGuru.h"
#import "cocoalib/Utils.h"

@implementation RecordingOptionsPage
- (id)init
{
    self = [super init];
    [self setTitle:@"Recording Options"];
    return self;
}

- (void)loadInfo:(NSMutableDictionary *)aInfo
{
    PyMusicGuru *py = [aInfo objectForKey:@"py"];
    [cdTable setPy:py];
}

- (void)saveInfo:(NSMutableDictionary *)aInfo
{
    long long mediaCapacity = [[aInfo objectForKey:@"MediaCapacity"] longLongValue];
    for (int i=0;i<[cdTable numberOfRows];i++)
    {
        NSArray *values = [[cdTable py] getTableView:i2n([cdTable tag]) valuesForRow:i2n(i)];
        double cdSize = [[values objectAtIndex:2] doubleValue];
        if ((cdSize * 1024 * 1024) > mediaCapacity)
            @throw [NSString stringWithFormat:@"'%@' is too big for your media capacity.",[values objectAtIndex:0]];
    }
    [aInfo setObject:b2n([addRecordedSwitch state] == NSOnState) forKey:@"AddRecorded"];
}
@end
