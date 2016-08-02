class Player():
    """
    Player object to be assoc with table seats dictionary

    ATTRIBUTES:

            @property {list} hole_cards List of players hole cards
            @property {int} stack Number of players chips left on table
            @property {bool} active Indicator for active status
            @property {string} table_name Unique table name assoc
            @property {int} equity Amount player has bet in round
            @property {bool} acted Has player acted in betting round
            @property {bool} action Is action currently on player
            @property {bool} missed_sb Indicates player missed small blind
            @property {bool} missed_bb Indicates player missed big blind

    METHODS:

            @method {} bet Add bet to equity and sub from stack
            @method {} fold Removes player from all pot objects
            @method {} quit Removes player from seats dict on table
            @method {} away Toggles players active status

     """
