/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import <Cocoa/Cocoa.h>

@interface WizPage : NSObject
{
    IBOutlet NSView *page;
@private
    NSString *_title;
}
- (void)loadInfo:(NSMutableDictionary *)aInfo;
- (void)saveInfo:(NSMutableDictionary *)aInfo;

- (NSView *)page;
- (NSString *)title;
- (void)setTitle:(NSString *)aTitle;
@end;

@interface Wizard : NSWindowController
{
    IBOutlet NSButton *cancelButton;
    IBOutlet NSView *customZone;
    IBOutlet NSTextField *frameTitleText;
    IBOutlet NSButton *nextButton;
    IBOutlet NSButton *previousButton;
    IBOutlet NSImageView *supportPicture;
    
    BOOL _atLastPage;
    int _blockPreviousAt;
    WizPage *_currentPage;
    id _delegate;
    NSMutableDictionary *_info;
    WizPage *_nonInteractivePage;
    int _pageIndex;
    NSMutableArray *_previousPages;
    NSModalSession _session;
}
- (id)initWithDelegate:(id)aDelegate;
- (void)dealloc;

- (IBAction)cancel:(id)sender;
- (IBAction)next:(id)sender;
- (IBAction)previous:(id)sender;

- (void)blockPrevious;
- (WizPage *)getNextPage;
- (BOOL)run;
- (void)runAsSession;
- (void)setCurrentPageAsLast;
- (void)setPage:(WizPage *)aPage;
- (void)setImage:(NSImage *)aPicture;
- (void)startNonInteractiveSessionWithPage:(WizPage *)aPage;
- (void)stopModalWithCode:(int)aCode;
- (void)stopNonInteractiveSession;
- (void)updateButtons;

- (WizPage *)currentPage;
- (NSMutableDictionary *)info;
- (int)pageIndex;
@end

@interface NSObject (WizardDelegate)
- (void)wizard:(Wizard *)aWizard ModalSessionEndedWithCode:(int)aCode;
- (WizPage *)wizardNeedsNextPage:(Wizard *)aWizard;
@end
