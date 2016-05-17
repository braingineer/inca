# inca: information curating agent

## overall idea
- a command line interface to various things
  + most notably: links, bibs, etc


## task stack management and constant reminders

- add task items 
    + `inca add task <task-name>`
- remove task items
    + `inca delete task <task-name`
- list task items
    + `inca list task`

### inside an i3blocks.conf:
```
[msg]
command=inca stack_iter task
interval=10
min_width=1920
align=center

```


### todo
1. nlu parser for dates
2. integration elsewhere (outside of i3blocks)