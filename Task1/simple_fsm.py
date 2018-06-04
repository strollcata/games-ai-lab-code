state = 'idle'
enemy_nearby = False
enemy_attacking = False
health = 3
enemy_health = 2
while state is not 'dead':
    if enemy_nearby is False:
        print('A warrior stands idle.')
        enemy_nearby = True
        enemy_health = 2
        print('An enemy appears!')
    if enemy_nearby is True:
            state = 'attacking'
    if state is 'attacking':
        print('The warrior attacks the enemy! The enemy loses 1 health.')
        enemy_health -= 1
        if enemy_health is 0:
            print('The enemy is vanquished!')
            state = 'idle'
            enemy_nearby = False
        else:
            state = 'defending'
    if state is 'defending':
        health -= 1
        print('The enemy strikes back! The warrior loses 1 health.')
        state = 'attacking'
    if health is 0:
        state = 'dead'
print('The warrior is dead. Please exit the program.')
