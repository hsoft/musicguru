#import "RegistrationRequiredPage.h"
#import <cocoalib/RegistrationInterface.h>
#import <cocoalib/Utils.h>
#import "Consts.h"

@implementation RegistrationRequiredPage

- (id)init
{
    self = [super init];
    [self setTitle:@"Registration Required"];
    return self;
}

- (IBAction)buyNow:(id)sender
{
    RegistrationInterface *ri = [[RegistrationInterface alloc] initWithAppName:APPNAME appId:APPID limitDescription:LIMIT_DESC];
    [ri buyNow:sender];
    [ri release];
}

- (IBAction)enterCode:(id)sender
{
    RegistrationInterface *ri = [[RegistrationInterface alloc] initWithAppName:APPNAME appId:APPID limitDescription:LIMIT_DESC];
    [ri enterCode];
    [ri release];
}

- (void)loadInfo:(NSMutableDictionary *)aInfo
{
    py = [aInfo objectForKey:@"py"];
}

- (void)saveInfo:(NSMutableDictionary *)aInfo
{
    if (![RegistrationInterface isAppIdRegistered:APPID])
        @throw @"You must purchase musicGuru before going any further.";
}

@end
