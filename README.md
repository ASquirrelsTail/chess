# Python Chess

Chess written in python.

To play a computer controlled opponent that makes legal moves at random run the play.py script, to make two random computer players compete pass the optional argument 'cpu'.

```
$ python play.py [cpu]
```

![alt text](https://raw.githubusercontent.com/ASquirrelsTail/chess/master/chess.png "The Black random computer controlled player beats the White computer controlled player.")
The result of two random computer controlled players. Black won, with an unusual check mate following bizzare stratergies from each side.

## To do

- Learn how to pass the state of the board and possible moves to a machine learning algorithm (this could take a while...).
- Make legal moves etc cache until the end of the turn. They don't currently, as they rely on each other and can be run in varying orders, which is slower, but safer.

## Simplifications

- A Pawn will always be promoted to a Queen to save having to make the choice.
- En Passant is ignored, as much because I never knew it was a rule of chess as because it's a pretty rare edge case.

## Testing

The piece behaviour was developed using test driven development, tests require unittest. Passing the optional -v verbose argument will print the board at the end of every test to help with debugging.

```
$ python -m unittest [-v]
```
