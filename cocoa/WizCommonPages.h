/* WizCommonPages */

#import <Cocoa/Cocoa.h>
#import "MessagePage.h"
#import "ProgressPage.h"

@interface WizCommonPages : NSObject
{
    IBOutlet MessagePage *messagePage;
    IBOutlet ProgressPage *progressPage;
}
- (MessagePage *)messagePage;
- (ProgressPage *)progressPage;
@end
