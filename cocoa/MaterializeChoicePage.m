/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "MaterializeChoicePage.h"
#import "cocoalib/Utils.h"
#import "PyMusicGuru.h"

@implementation MaterializeChoicePage
- (id)init
{
    self = [super init];
    [self setTitle:@"Materialize Type"];
    return self;
}

- (void)saveInfo:(NSMutableDictionary *)aInfo
{
    PyMusicGuru *py = [aInfo objectForKey:@"py"];
    int materializeType = [typeSelector selectedRow];
    [aInfo setObject:i2n(materializeType) forKey:@"MaterializeType"];
    if ((materializeType == 0) && (![[py locationNamesInBoard:b2n(YES) writable:b2n(YES)] count]))
        @throw @"You cannot choose this option with read-only locations.";
    if ((materializeType == 3) && (!n2b([py isBoardSplitted])))
        @throw @"You must split your Design Board into CD before recording it.";
}
@end
