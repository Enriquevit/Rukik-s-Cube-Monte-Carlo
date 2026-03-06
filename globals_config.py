"""
globals_config.py

Global configuration and state variables for CFOP and cross solving.
"""

# Cross color (default: white)
CROSS_COLOR = 'W'

# Skill levels
CROSS_SKILL = 'beginner'  # 'beginner', 'intermediate', 'advanced'
F2L_SKILL = 0             # 0=beginner, 1=intuitive, 2=efficient, 3=advanced
OLL_SKILL = 2             # 1=2-look, 2=1-look
PLL_SKILL = 2             # 1=2-look, 2=1-look

# Number of moves in scramble (to be set by scramble generator)
SCRAMBLE_LENGTH = 20
