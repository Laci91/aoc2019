def check_position_in_list(position, checked_list):
    if position >= len(checked_list):
        raise Exception('Position %d falls outside of the list index range (0-%d)' % (position, len(checked_list)))
