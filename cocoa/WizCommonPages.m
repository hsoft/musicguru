/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

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
