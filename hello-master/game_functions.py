import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets, music):
    """响应案件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, music)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets, music):
    """发子弹"""
    # 创建一颗子弹,加入编组
    if len(bullets) < ai_settings.bullet_allowed:
        music.boom.play()
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, music):
    """先听按键鼠标"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, music)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            # 重置设置
            ai_settings.initialize_dynamic_settings()

            # 隐藏光标
            pygame.mouse.set_visible(False)


            # 重置信息
            stats.reset_stats()
            stats.game_active = True

            aliens.empty()
            ai_settings.increase_speed()
            bullets.empty()

            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()

            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            sb.prep_ships()
        else:
            pygame.mouse.set_visible(True)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """更新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # 现实得分
    sb.show_score()

    if not stats.game_active:
        play_button.draw_exit_button()
        play_button.draw_button()


    # 让最近的绘制可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置，删除消失子弹"""
    # 更新位置
    bullets.update()

    # 删除子弹
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))

    check_bullet_alien_collisions(ai_settings,  bullets, aliens, stats, sb)

    # 删外星人
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open(" record/high_score.txt", "w") as high:
            high.write(str(stats.score))


def check_bullet_alien_collisions(ai_settings, bullets, aliens, stats, sb):
    # 检查子弹
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)


def get_number_x(ai_settings, alien_width):
    """外星群"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """外星群"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_aliens_rows = int(available_space_y / (2 * alien_height))
    return number_aliens_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    if stats.ship_left > 0:
        stats.ship_left -= 1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)

    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False
        print("ship hit!!!")


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """更新所有位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
