/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "InsertBlankDiskPage.h"
#import "../cocoalib/Utils.h"
#import "PyMusicGuru.h"

@implementation InsertBlankDiskPage
- (id)init
{
    self = [super init];
    [self setTitle:@"Blank Disc Needed"];
    return self;
}

- (void)loadInfo:(NSMutableDictionary *)aInfo
{
    PyMusicGuru *py = [aInfo objectForKey:@"py"];
    [messageLabel setStringValue:[NSString stringWithFormat:@"Please insert a blank CD. It will be labeled '%@'",[py getDestinationDiskName]]];
    [py ejectCDIfNotBlank];
}

- (void)saveInfo:(NSMutableDictionary *)aInfo
{
    PyMusicGuru *py = [aInfo objectForKey:@"py"];
    if (!n2b([py ejectCDIfNotBlank]))
        @throw @"You must insert a blank CD in your drive before continuing.";
}

@end
