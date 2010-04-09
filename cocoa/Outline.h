/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>
#import "PyMusicGuru.h"

@interface OVNode: NSObject
{
    NSArray *_buffer;
    NSMutableArray *_children;
    NSInteger _index;
    NSIndexPath *_indexPath;
    NSInteger _marked;
    NSInteger _ovTag;
    NSInteger _level;
    NSInteger _maxLevel;
    OVNode *_parent;
    PyMusicGuru *_py;
}
// childrenCount == -1 if you don't know
- (id)initWithParent:(OVNode *)aParent index:(NSInteger)aIndex childrenCount:(NSInteger)aChildrenCount;
- (void)dealloc;

- (OVNode *)getChildAtIndex:(NSInteger)aIndex;
- (OVNode *)nodeAtPath:(NSIndexPath *)path;
- (void)invalidateMarkingRecursively:(BOOL)aRecursive;
- (BOOL)isMarked;
- (BOOL)isMarkable;
- (NSInteger)level;
- (NSInteger)maxLevel;
- (NSInteger)childrenCount;
- (void)resetAllBuffers;

- (NSArray *)buffer;
- (void)setBuffer:(NSArray *)aBuffer;
- (NSInteger)index;
- (NSIndexPath *)indexPath;
- (OVNode *)parent;

- (NSInteger)tag;
- (void)setTag:(NSInteger)aNewTag;
- (PyMusicGuru *)py;
- (void)setPy:(PyMusicGuru *)aNewPy;
@end

@interface ArrowlessBrowserCell : NSBrowserCell
@end;

@interface OutlineView : NSOutlineView
{
    IBOutlet PyMusicGuru *py;
    
    OVNode *_root;
}
- (void)doInit;
- (NSInteger)outlineView:(NSOutlineView *)outlineView numberOfChildrenOfItem:(id)item;
- (id)outlineView:(NSOutlineView *)outlineView objectValueForTableColumn:(NSTableColumn *)tableColumn byItem:(id)item;
- (id)outlineView:(NSOutlineView *)outlineView child:(NSInteger)index ofItem:(id)item;
- (BOOL)outlineView:(NSOutlineView *)outlineView isItemExpandable:(id)item;
/* Public */
- (OVNode *)findNodeWithName:(NSString *)aName inParentNode:(OVNode *)aParentNode;
- (void)invalidateBuffers;
- (void)invalidateMarkings;
- (void)makeImagedColumnWithId:(NSString *)aId;
- (NSArray *)selectedNodes;
- (NSArray *)selectedNodePaths;
- (void)selectNodePaths:(NSArray *)nodePaths;

/* Properties */
- (PyMusicGuru *)py;
- (void)setPy:(PyMusicGuru *)aPy;
@end

@interface DraggableOutlineView : OutlineView
{
    NSArray *_draggedNodes;
}
/* Virtual */
- (NSColor *)determineDragCircleColor;
- (NSArray *)determineDraggedNodesForDraggedRow:(NSInteger)aDraggedRow;
- (NSImage *)determineDragImage;
- (BOOL)performDragFrom:(DraggableOutlineView *)aSource withNodes:(NSArray *)aSourceNodes to:(OVNode *)aDestNode;

/* Properties */
- (NSArray *)draggedNodes;
- (void)setDraggedNodes:(NSArray *)aNodes;
@end

@protocol DraggableOutlineViewDelegate
- (void)outlineView:(DraggableOutlineView *)aDest draggedFrom:(DraggableOutlineView *)aDest;
@end
