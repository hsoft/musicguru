/* 
Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "Wizard.h"
#import "../cocoalib/Dialogs.h"

@implementation WizPage
- (id)init
{
    self = [super init];
    _title = nil;
    [self setTitle:@""];
    return self;
}

- (void)dealloc
{
    [self setTitle:nil];
    [super dealloc];
}

- (void)loadInfo:(NSMutableDictionary *)aInfo
{
}

- (void)saveInfo:(NSMutableDictionary *)aInfo;
{
}

- (NSView *)page {return page;}
- (NSString *)title {return _title;}
- (void)setTitle:(NSString *)aTitle
{
    if (_title)
        [_title release];
    _title = [aTitle retain];
}
@end

@implementation Wizard
- (id)initWithDelegate:(id)aDelegate
{
    self = [super initWithWindowNibName:@"wizard"];
    [self window];
    _delegate = aDelegate;
    _info = [[NSMutableDictionary dictionary] retain];
    _previousPages = [[NSMutableArray array] retain];
    _currentPage = nil;
    _nonInteractivePage = nil;
    _session = nil;
    _pageIndex = -1;
    _blockPreviousAt = 0;
    _atLastPage = NO;
    return self;
}

- (void)dealloc
{
    [_info release];
    [_previousPages release];
    if (_currentPage)
        [_currentPage release];
    [super dealloc];
}

- (IBAction)cancel:(id)sender
{
    [[self window] performClose:sender];
}

- (IBAction)next:(id)sender
{
    if (_currentPage)
    {
        @try
        {
            [_currentPage saveInfo:_info];
        }
        @catch (NSString *e)
        {
            [Dialogs showMessage:e];
            return;
        }
    }
    if (_atLastPage)
    {
        [self stopModalWithCode:NSOKButton];
        return;
    }
    WizPage *nextPage = [self getNextPage];
    if (!nextPage)
    {
        [self stopModalWithCode:NSCancelButton];
        return;
    }
    _pageIndex++;
    [nextPage loadInfo:_info];
    if (_currentPage)
        [_previousPages addObject:_currentPage];
    [self setPage:nextPage];
    [self updateButtons];
}

- (IBAction)previous:(id)sender
{
    if (![_previousPages count])
        return;
    WizPage *prevPage = [_previousPages lastObject];
    [_previousPages removeLastObject];
    _pageIndex--;
    _atLastPage = NO;
    [self setPage:prevPage];
    [self updateButtons];
}

- (void)blockPrevious
{
    _blockPreviousAt = _pageIndex + 1;
}

- (WizPage *)getNextPage
{
    return [_delegate wizardNeedsNextPage:self];
}

- (BOOL)run
{
    //Returns YES if the wizard user has clicked the Finish button.
    [self next:self];
    return ([NSApp runModalForWindow:[self window]] == NSOKButton);
}

- (void)runAsSession
{
    [self next:self];
    _session = [NSApp beginModalSessionForWindow:[self window]];
}

- (void)setCurrentPageAsLast
{
    _atLastPage = YES;
    [self updateButtons];
}

- (void)setPage:(WizPage *)aPage
{
/*
 Some things here must be understood and REMEMBERED about customZone and sub views.
 customZone is a NSBox. When calling subviews() in an empty customZone, there apparently
 is 1 sub view. When adding a sub view to the NSBox with addSubview, there is still only
 1 object in subviews(). That is because the view is not added to the NSBox itself, but
 to it's only NSView children. Thus, what I understand of it is that the first children
 of the NSBox is the content view, and it is in this view that we must check if the content
 is there (in test units). I write this because I fucked around a lot with this I don't
 want to do it again (in case I forget about this.).
*/
    if (_currentPage)
    {
        [[_currentPage page] removeFromSuperview];
        [_currentPage release];
    }
    _currentPage = [aPage retain];
    [frameTitleText setStringValue:[aPage title]];
    [customZone addSubview:[aPage page]];
    [[aPage page] setFrame:NSMakeRect(0,0,[customZone frame].size.width,[customZone frame].size.height)];
    //Set key order
    NSView *first = [[aPage page] nextKeyView];
    if (first)
    {
        //Warning Don't make loops in your key views, or you will have infinite loop here.
        NSView *current = first;
        while (([current nextKeyView]) && ([current nextKeyView] != first) && ([current nextKeyView] != cancelButton))
            current = [current nextKeyView];
        [nextButton setNextKeyView:first];
        [current setNextKeyView:cancelButton];
        [[self window] makeFirstResponder:first];
    }
    else
        [[self window] makeFirstResponder:nextButton];
}

- (void)setImage:(NSImage *)aPicture
{
    [supportPicture setImage:aPicture];
}

- (void)startNonInteractiveSessionWithPage:(WizPage *)aPage
{
    _nonInteractivePage = [aPage retain];
    [[_currentPage page] removeFromSuperview];
    [frameTitleText setStringValue:[aPage title]];
    [customZone addSubview:[aPage page]];
    [[aPage page] setFrame:NSMakeRect(0,0,[customZone frame].size.width,[customZone frame].size.height)];
    [previousButton setEnabled:NO];
    [nextButton setEnabled:NO];
}

- (void)stopModalWithCode:(int)aCode
{
    if (_session)
    {
        [NSApp endModalSession:_session];
        [[self window] close];
        [_delegate wizard:self ModalSessionEndedWithCode:aCode];
    }
    else
    {
        [NSApp stopModalWithCode:aCode];
        [[self window] close];
    }
}

- (void)stopNonInteractiveSession
{
    if (!_nonInteractivePage)
        return;
    [[_nonInteractivePage page] removeFromSuperview];
    [frameTitleText setStringValue:[_currentPage title]];
    [customZone addSubview:[_currentPage page]];
    [[_currentPage page] setFrame:NSMakeRect(0,0,[customZone frame].size.width,[customZone frame].size.height)];
    [_nonInteractivePage release];
    _nonInteractivePage = nil;
    [self updateButtons];
}

- (void)updateButtons
{
    [previousButton setEnabled:_pageIndex > _blockPreviousAt];
    if (_atLastPage)
        [nextButton setTitle:@"Finish"];
    else
        [nextButton setTitle:@"Next >>"];
    [nextButton setEnabled:YES];
}

//Delegate
- (BOOL)windowShouldClose:(id)sender
{
    return [Dialogs askYesNo:@"Do you really want to cancel this wizard?"] == NSAlertFirstButtonReturn;
}

- (void)windowWillClose:(NSNotification *)aNotification
{
    [self stopNonInteractiveSession];
    if ([NSApp modalWindow])
        [self stopModalWithCode:NSCancelButton];
}

//Properties
- (WizPage *)currentPage {return _currentPage;}
- (NSMutableDictionary *)info {return _info;}
- (int)pageIndex {return _pageIndex;}
@end
