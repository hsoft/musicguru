#import "MaterializeChoicePage.h"
#import <cocoalib/Utils.h>
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
