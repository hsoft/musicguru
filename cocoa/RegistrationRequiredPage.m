/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "RegistrationRequiredPage.h"
#import "cocoalib/RegistrationInterface.h"
#import "cocoalib/Utils.h"
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
    RegistrationInterface *ri = [[RegistrationInterface alloc] initWithApp:py name:APPNAME limitDescription:LIMIT_DESC];
    [ri buyNow:sender];
    [ri release];
}

- (IBAction)enterCode:(id)sender
{
    RegistrationInterface *ri = [[RegistrationInterface alloc] initWithApp:py name:APPNAME limitDescription:LIMIT_DESC];
    [ri enterCode];
    [ri release];
}

- (void)loadInfo:(NSMutableDictionary *)aInfo
{
    py = [aInfo objectForKey:@"py"];
}

- (void)saveInfo:(NSMutableDictionary *)aInfo
{
    if (![py isRegistered])
        @throw @"You must purchase musicGuru before going any further.";
}

@end
