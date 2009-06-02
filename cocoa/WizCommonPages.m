#import "WizCommonPages.h"

@implementation WizCommonPages
- (id)init
{
    self = [super init];
    [NSBundle loadNibNamed:@"wiz_common" owner:self];
    return self;
}

- (MessagePage *)messagePage {return messagePage;}
- (ProgressPage *)progressPage {return progressPage;}
@end
