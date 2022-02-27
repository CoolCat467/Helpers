#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Client Sprite and Renderer

"Client Sprite and Renderer"

# Programmed by CoolCat467

from typing import Union, Callable, Iterable
import asyncio

from pygame.sprite import DirtySprite, LayeredDirty
from pygame.rect import Rect# pylint: disable=no-name-in-module
from pygame.event import event_name

from vector import Vector2
from client_runstater import Runner, EventAsyncState
from events import Event
##from event_statetimer import EventAsyncState

__title__ = 'Client Sprite'
__author__ = 'CoolCat467'
__version__ = '0.0.0'

class Location(Vector2):
    "Location bound to the center of a given rect"
    __slots__ = ('_rect',)
    # typecheck: error: "__new__" must return a class instance (got "Union[Location, Vector2]")
    def __new__(cls, *args, dtype=None) -> Union['Location', Vector2]:
        "Super hack to return Vector2 if dtype is not None, otherwise new Location."
        if dtype is not None:
            new_vec = Vector2.__new__(Vector2)
            # typecheck: error: Cannot access "__init__" directly
            new_vec.__init__(*args, dtype=dtype)
            return new_vec
        return super().__new__(cls)
    
    def __init__(self, rect: Rect) -> None:
        "Initialize Location with rect."
        self._rect = rect
        super().__init__(*self._rect.center, dtype=list)
    
    # typecheck: note: "__setitem__" of "Location" defined here
    def __setitem__(self, index: int, value: Union[int, float], normal: bool=False):
        "Setitem, but if not normal, updates rect as well."
        super().__setitem__(index, value)
        if normal:
            return
        # typecheck: note:     def [_T] iter(Callable[[], _T], object) -> Iterator[_T]
        self._rect.center = tuple(iter(self))
    
    def __getitem__(self, index: int) -> Union[int, float]:
        "Getitem, but sets internal data at index to data from rect center first."
        # typecheck: error: Unexpected keyword argument "normal" for "__setitem__" of "Location"
        self.__setitem__(index, self._rect.center[index], normal=True)
        # typecheck: error: Incompatible return value type (got "Union[int, float, complex]", expected "Union[int, float]")
        return super().__getitem__(index)
    
    # typecheck: error: Return type "None" of "normalize" incompatible with return type "Vector" in supertype "Vector"
    def normalize(self) -> None:
        "Raise NotImplemented, original is in place."
        raise NotImplementedError
    
    # typecheck: note:          def set_length(self, new_length: Any = ...) -> None
    def set_length(self, new_length=None) -> None:
        "Raise NotImplemented, original is in place."
        raise NotImplementedError

class ClientSprite(DirtySprite):
    """Client sprite class.
    
    Optional ability to define on_event and on_click async functions, but
    don't do it for no reason, skips processing if it doesn't exist,
    so therefore faster if nothing needed."""
    __slots__ = ('rect', '__location', '__image')
    def __init__(self, *groups):
        super().__init__(*groups)
        
        self.__image = None
        self.rect = Rect(0, 0, 0, 0)
        self.__location = Location(self.rect)
        
    # pylint: disable=unused-private-member
    def __get_location(self) -> Location:
        return self.__location
    def __set_location(self, value: Iterable) -> None:
        # typecheck: error: Value of type "Iterable[Any]" is not indexable
        self.__location.x = value[0]
        # typecheck: error: Value of type "Iterable[Any]" is not indexable
        self.__location.y = value[1]
    
    location = property(__get_location, __set_location, doc='Location')
    
    def __get_image_dims(self):
        return self.rect.size
    def __set_image_dims(self, value):
        pre_loc = self.location
        self.rect.size = value
        self.location = pre_loc
    
    image_dims = property(__get_image_dims, __set_image_dims, doc='Image dimentions')
    
    def __get_image(self):
        return self.__image
    def __set_image(self, image) -> None:
        "Set image, update image_dims"
        self.__image = image
        self.image_dims = image.get_size()
    
    # typecheck: error: Incompatible types in assignment (expression has type "property", base class "Sprite" defined the type as "Optional[Surface]")
    image = property(__get_image, __set_image, doc='Image property auto-updating dimentions.')
    
##    async def on_event(self, event) -> None:
##        "Process an event"
    
    def update(self, time_passed: float) -> None:# pylint: disable=arguments-differ
        "Update with time_passed"

class SubRenderer(LayeredDirty):
    "Gear Runner and Layered Dirty Sprite group"
    __slots__: tuple = tuple()
    async def handle_event(self, event):
        "Process on_click handlers for sprites on mouse down events."
        coros = []
        for sprite in self.sprites():
            if hasattr(sprite, 'on_event'):
                coros.append(sprite.on_event(event))
        if event.type == 'MouseButtonDown' and event['button'] == 1:
            sprites = self.get_sprites_at(event['pos'])
            layers = tuple(sorted(
                {sprite.layer for sprite in sprites},
                reverse=True))
            for layered_sprite in sprites:
                if hasattr(layered_sprite, 'on_click'):
                    coros.append(
                        layered_sprite.on_click(
                            layers.index(layered_sprite.layer)
                        )
                    )
        await asyncio.gather(*coros)

class GroupGearProcessor(Runner):
    "Gear Runner and Layered Dirty Sprite group handler"
    __slots__ = ('config', 'groups', 'group_names', 'new_gid', '_timing', '_clear')
    def __init__(self, event_loop, config, language):
        super().__init__(event_loop)
        
        self.conf = config
        self.lang = language
        
        self.groups = {}
        self.group_names = {}
        self.new_gid = 0
        self._timing = 1000/80
        self._clear = None, None
    
    def clear(self, screen, background):
        "clear for all groups"
        self._clear = screen, background
        for group in self.groups.values():
            group.clear(*self._clear)
    
    def set_timing_treshold(self, value: float) -> None:
        "set_timing_treshold for all groups"
        self._timing = value
        for group in self.groups.values():
            group.set_timing_treshold(self._timing)
    
    def new_group(self, name: str=None) -> int:
        "Make a new group and return id"
        if name is not None:
            self.group_names[name] = self.new_gid
        self.groups[self.new_gid] = SubRenderer()
        self.groups[self.new_gid].set_timing_treshold(self._timing)
        if self._clear[1] is not None:
            self.groups[self.new_gid].clear(*self._clear)
        self.new_gid += 1
        return self.new_gid-1
    
    def remove_group(self, gid: int) -> None:
        "Remove group"
        if gid in self.groups:
            del self.groups[gid]
            for name, v_gid in self.group_names.items():
                if v_gid == gid:
                    # pylint: disable=unnecessary-dict-index-lookup
                    del self.group_names[name]
                    return
    
    def get_group(self, gid_name: Union[str, int]) -> Union[SubRenderer, None]:
        "Return group from gid"
        named = None
        if isinstance(gid_name, str):
            named = gid_name
            if gid_name in self.group_names:
                gid_name = self.group_names[gid_name]
        if gid_name in self.groups:
            return self.groups[gid_name]
        if named is not None:
            del self.group_names[named]
        return None
    
    def send_pygame_event(self, py_event) -> None:
        "Send py event to event loop, adding pygame_event_prefix to name."
        name = event_name(py_event.type)
        self.submit_event(Event(name, **py_event.dict))
    
    async def proc_additional_handlers(self, event: Event) -> None:
        "Process sprites with on_event handlers."
        await super().proc_additional_handlers(event)
        coros = []
        for group in self.groups.values():
            coros.append(group.handle_event(event))
        
        await asyncio.gather(*coros)
    
    async def update(self, time_passed: float) -> None:
        "Process gears and update sprites"
        for group in self.groups.values():
            group.update(time_passed)
        await self.process()
    
    def draw(self, screen) -> list[Rect]:
        "Draw all groups"
        rects = []
        for group in self.groups.values():
            rects.extend(group.draw(screen))
        return rects

class RenderClientState(EventAsyncState):
    "Client state with a renderer"
    __slots__ = ('group', 'hault', 'is_new_group')
    keep_newgroup = False
    def __init__(self, name: str):
        super().__init__(name)
        
        # typecheck: error: Incompatible types in assignment (expression has type "None", variable has type "int")
        self.group: int = None
        self.hault: bool = False
        self.is_new_group: bool = False
    
    @property
    def renderer(self):
        "Group render"
        if self.group is None:
            self.is_new_group = True
            self.group = self.machine.new_group(self.name)
        return self.machine.get_group(self.group)
    
    @property
    def conf(self):
        "Configuration from client."
        return self.machine.conf
    
    @property
    def lang(self):
        "Language from client."
        return self.machine.lang
    
    async def on_event(self, event) -> None:
        if event.type == 'UserEvent':
            if event['event'] == 'escape':
                self.hault = True
    
    # typecheck: error: Missing return statement
    async def check_conditions(self) -> Union[str, None]:
        if self.hault:
            return 'Hault'
    
    async def exit_actions(self) -> None:
        "Remove new group if not keep new groups."
        self.hault = False
        if not self.keep_newgroup and self.is_new_group:
            self.renderer.empty()
            # typecheck: error: "AsyncStateMachine" has no attribute "remove_group"
            self.machine.remove_group(self.group)
            self.is_new_group = False
            # typecheck: error: Incompatible types in assignment (expression has type "None", variable has type "int")
            self.group = None

class MenuClientState(RenderClientState):
    "Menu state"
    __slots__ = ('next_state',)
    def __init__(self, name: str):
        super().__init__(name)
        
        self.next_state = None
    
    def set_state(self, name: str) -> Callable:
        "Set state"
        def set_state_wrapper() -> None:
            "Set next state"
            # typecheck: error: Incompatible types in assignment (expression has type "str", variable has type "None")
            self.next_state = name
        return set_state_wrapper
    
    async def check_conditions(self) -> Union[str, None]:
        "Hault if self.hault, otherwise self.next_state"
        if self.hault:
            return 'Hault'
        if self.next_state:
            return self.next_state
        return None
    
    async def exit_actions(self) -> None:
        await super().exit_actions()
        self.next_state = None

def run():
    "Run test"





if __name__ == '__main__':
    print(f'{__title__}\nProgrammed by {__author__}.')
    run()
