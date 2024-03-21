# Caro
## A project for Project-1-hust-20231

## Trying to use Reinforcement Learning and success

This project implemented the basic (I prefer to call 'naive' since it's the simplest) Q-Learning agents to play Caro a.k.a Gomoku game.

Using two agents with seperated Q table to save the game state and its Q value. In this project, I json-ed the states then hash them.

Although I think the hash approach is kind of risky but with a pretty large board, I have no choice because SQL server cannot use above 1000 characters with varchar datatype.

I trained them to play with a specific style. It's a sort of heuristics which is playing the moves that are neighbour with the 'fighting'. I know it's not optimal but it helped me training the agents much faster.

I use complete search to check the specific moves to win or defense as well. I think it makes sense because in this game, we always block the potential 4 in a row imediately if that 4 in a row is opened two side. The 'AI part' is only the strategy of play.

