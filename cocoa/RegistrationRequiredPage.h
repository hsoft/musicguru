/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>
#import "Wizard.h"
#import "PyMusicGuru.h"

@interface RegistrationRequiredPage : WizPage
{
    PyMusicGuru *py;
}
- (IBAction)buyNow:(id)sender;
- (IBAction)enterCode:(id)sender;
@end
