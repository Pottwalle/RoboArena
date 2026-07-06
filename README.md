# RoboArena
### Steuerung
> `[W] -> move up`\
> `[S] -> move down`\
> `[A] -> move left`\
> `[D] -> move right`\
>
> ingame:\
> `[ESC] -> enters escape menu`
> `[I] -> enters / exits the Inventory`
>
> in inventory:\
> `[RMB] -> equips / unequips item in inventory`
>
> in escape menu:\
> `[ESC] -> exits escape menu`
>
> in settings menu:\
> `[ESC] -> exits to main menu`

### GitHub IO Page: 
> https://pottwalle.github.io/RoboArena/

### add Items
> use the [Item Creator](https://github.com/Pottwalle/RoboArena/pull/103)
> 1. enter an `item_id` which is the key used in the game to acess the item later
>    - the game automatically creates the `Item name` from the `id`, but can be changed manually
> 2. `Description` can be added though currently is not displayed ingame
> 3. Select an `equipment slot`, if the Item has the Type `equipment`
> 4. select `type` of the item, which determines the class used ingame, only items can hold stats & equipment slots
> 5. enter the `sprite sheet coordinates` which are the `pixel values` on the sprite sheer `(x, y)` where the texture for the item can be found, should be inside the sprite sheet
> 6. if the type is `equipment` you now can add `stats` whith the button `Add Stats`
> 7. each stat consist of a `stat_id` a stat value which is a `float` but gets changed to int if its even
>    - the delete stat button also removes the stat again
> 8. `Save to Json` saves / updates the item in the `items.json` file

### Sprint 1: Space Invaders Project
> Branch: [test/space-invaders-target](https://github.com/Pottwalle/RoboArena/tree/test/space-invaders-target)

### Quellen:
> Hauptmenü Hintergrund wurde mit Google Gemini erstellt
