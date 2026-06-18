import argparse
from manager import Manager


def main():
    parser = argparse.ArgumentParser(description="Play the Khet game")
    parser.add_argument('config_file',
                        type=str,
                        help='Path to the config file')
    parser.add_argument('--draw-detection', action='store_true')
    parser.add_argument(
        '--win-detection',
        type=int,
        help='Search depth for forced win detection')
    args = parser.parse_args()
    config_file_path = args.config_file

    manager = Manager(config_file_path)
    manager.set_enable_draw(args.draw_detection)

    manager._prepare_outfile(config_file_path)
    manager.readFile()

    if args.win_detection is not None:
        result = manager.find_forced_win_depth1()
        manager.write_error_to_outfile(
            config_file_path,
            "true" if result else "false",
            False)
        return

    outt = manager.generate_initial_state_string()
    manager.write_initial_state_to_outfile(config_file_path, outt)
    in_game = True
    current_player = 1
    count = 0

    while in_game:
        player_num = 0
        player_letter = 'A'

        if current_player == 1:
            player_num = 1
            player_letter = 'A'
        elif current_player == -1:
            player_num = 2
            player_letter = 'B'

        manager.write_error_to_outfile(
            config_file_path,
            f"\nPlayer {player_num} move:\n",
            False)
        player_input = input().strip()

        if player_input == 'q':
            players_move = (
                f"Player {player_num} performed the move {player_input}")
            manager.write_error_to_outfile(config_file_path,
                                           players_move,
                                           False)
            manager.write_error_to_outfile(config_file_path,
                                           f"The game ended via quit",
                                           False)
            exit(0)

        while not manager.check_move(player_input, player_letter):
            manager.write_error_to_outfile(config_file_path,
                                           f"Player {player_num} move:\n",
                                           False)
            player_input = input().strip()
            if player_input == 'q':
                players_move = (
                    f"Player {player_num} performed the move {player_input}")
                manager.write_error_to_outfile(config_file_path,
                                               players_move,
                                               False)
                manager.write_error_to_outfile(config_file_path,
                                               f"The game ended via quit",
                                               False)
                exit(0)

        manager.apply_move(player_input, player_letter)

        players_move = f"Player {player_num} performed the move {player_input}"
        manager.write_error_to_outfile(config_file_path,
                                       players_move,
                                       False)
        new_out = manager.generate_initial_state_string()
        manager.write_error_to_outfile(config_file_path, new_out, False)

        if manager.game_over:
            if manager.winner is None and args.draw_detection:
                i, j, k = manager.draw_indices
                manager.write_error_to_outfile(
                    config_file_path,
                    "\nGame ended in draw due to repetition of "
                    f"game state {i}, {j}, {k}",
                    False)
            in_game = False
            break

        current_player *= -1

    if manager.winner is not None:
        manager.write_error_to_outfile(config_file_path,
                                       f"\nPlayer {manager.winner} won",
                                       False)

if __name__ == '__main__':
    main()
