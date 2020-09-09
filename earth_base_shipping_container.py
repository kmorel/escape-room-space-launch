import pygame

class ShippingContainer(pygame.sprite.Sprite):
    def platform2x(self, platform):
        return self.container_x_0 + (platform * self.container_width)

    def height2y(self, stack_height):
        return self.container_base_y - (stack_height * self.container_height)

    def __init__(self, number, platform, stack_height):
        pygame.sprite.Sprite.__init__(self)
        image_file = \
            'images/earth-base/shipping-container-{}.png'.format(number)
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()

        self.speed = 10
        self.container_height = 100
        self.container_width = 388

        self.container_base_y = 600
        self.container_lift_y = \
            self.container_base_y - (3.1*self.container_height)

        self.container_x_0 = 400

        self.rect.midbottom = \
            (self.platform2x(platform), self.height2y(stack_height))

        self.STATE_STOP = 0
        self.STATE_MOVE_UP = 1
        self.STATE_MOVE_LEFT = 2
        self.STATE_MOVE_RIGHT = 3
        self.STATE_MOVE_DOWN = 4
        self.state = self.STATE_STOP

        self.platform = platform
        self.stack_height = stack_height

    def move_to(self, platform, stack_height):
        self.platform = platform
        self.stack_height = stack_height
        self.state = self.STATE_MOVE_UP

    def update(self):
        target_x = self.platform2x(self.platform)
        target_y = self.height2y(self.stack_height)
        if self.state == self.STATE_MOVE_UP:
            self.rect.y -= self.speed
            if self.rect.bottom <= self.container_lift_y:
                self.rect.bottom = self.container_lift_y
                if target_x < self.rect.centerx:
                    self.state = self.STATE_MOVE_LEFT
                else:
                    self.state = self.STATE_MOVE_RIGHT
        elif self.state == self.STATE_MOVE_LEFT:
            self.rect.x -= self.speed
            if self.rect.centerx <= target_x:
                self.rect.centerx = target_x
                self.state = self.STATE_MOVE_DOWN
        elif self.state == self.STATE_MOVE_RIGHT:
            self.rect.x += self.speed
            if self.rect.centerx >= target_x:
                self.rect.centerx = target_x
                self.state = self.STATE_MOVE_DOWN
        elif self.state == self.STATE_MOVE_DOWN:
            self.rect.y += self.speed
            if self.rect.bottom >= target_y:
                self.rect.bottom = target_y
                self.state = self.STATE_STOP


