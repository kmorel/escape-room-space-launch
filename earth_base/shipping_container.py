import panda3d.core
import direct.task.Task
import direct.task.TaskManagerGlobal

import panda3d_utils


class ShippingContainer:
    def platform2x(self, platform):
        return self.container_x_0 + (platform * self.container_spacing)

    def height2y(self, stack_height):
        return self.container_base_y + (stack_height * self.container_height)

    def __init__(self, base, number, platform, stack_height):
        self.number = number
        image_file = \
            'images/earth_base/shipping-container-{}.png'.format(number)
        texture = base.loader.loadTexture(image_file)
        ratio = texture.getOrigFileXSize()/texture.getOrigFileYSize()

        self.depth = 0

        self.container_height = 0.2
        self.container_spacing = 3.88*self.container_height

        self.container_base_y = -0.5
        self.container_lift_y = \
            self.container_base_y + (3.1*self.container_height)

        self.container_x_0 = -1.0

        self.speed = 0.6

        self.node = base.render.attachNewNode(
            panda3d_utils.make_billboard(image_file))
        self.node.setTexture(texture)
        self.node.setScale(
            ratio*self.container_height, self.container_height, 1)
        self.node.setPos(
            self.platform2x(platform), self.height2y(stack_height), self.depth)

        self.platform = platform
        self.stack_height = stack_height

    def move_to(self, platform, stack_height):
        self.platform = platform
        self.stack_height = stack_height
        self.last_position = self.node.getPos()
        direct.task.TaskManagerGlobal.taskMgr.add(
            self.move_up_task, 'move-container')

    def move_up_task(self, task):
        current_pos = self.node.getPos()
        start_y = self.last_position[1]
        next_y = start_y + (task.time * self.speed)
        target_y = self.container_lift_y
        if next_y < target_y:
            self.node.setPos(current_pos[0], next_y, current_pos[2])
            return direct.task.Task.cont
        else:
            self.node.setPos(current_pos[0], target_y, current_pos[2])
            target_x = self.platform2x(self.platform)
            direction = -1 if target_x < current_pos[0] else 1
            direct.task.TaskManagerGlobal.taskMgr.add(
                self.move_sideways_task, 'move-container')
            return direct.task.Task.done

    def move_sideways_task(self, task):
        current_pos = self.node.getPos()
        target_x = self.platform2x(self.platform)
        direction = -1 if target_x < self.last_position[0] else 1
        start_x = self.last_position[0]
        next_x = start_x + (direction * task.time * self.speed)
        if (next_x * direction) < (target_x * direction):
            self.node.setPos(next_x, current_pos[1], current_pos[2])
            return direct.task.Task.cont
        else:
            self.node.setPos(target_x, current_pos[1], current_pos[2])
            direct.task.TaskManagerGlobal.taskMgr.add(
                self.move_down_task, 'move-container')
            return direct.task.Task.done

    def move_down_task(self, task):
        current_pos = self.node.getPos()
        start_y = self.container_lift_y
        next_y = start_y - (task.time * self.speed)
        target_y = self.height2y(self.stack_height)
        if next_y > target_y:
            self.node.setPos(current_pos[0], next_y, current_pos[2])
            return direct.task.Task.cont
        else:
            self.node.setPos(current_pos[0], target_y, current_pos[2])
            return direct.task.Task.done


class ContainerStacks:
    def __init__(self, base):
        self.stacks = [[], [], []]
        for container_id in range(4):
            container = ShippingContainer(
                base, 4 - container_id, 0, container_id)
            self.stacks[0].append(container)
        self.move_sound = base.loader.loadSfx('audio/hydraulic-lift.ogg')

    def can_move(self, start_stack, end_stack):
        if len(self.stacks[start_stack]) < 1:
            return False
        if len(self.stacks[end_stack]) < 1:
            return True
        return (self.stacks[start_stack][-1].number <
                self.stacks[end_stack][-1].number)

    def move(self, start_stack, end_stack):
        if not self.can_move(start_stack, end_stack):
            print('Invalid move: {} -> {}'.format(start_stack, end_stack))
            return
        container = self.stacks[start_stack].pop()
        container.move_to(end_stack, len(self.stacks[end_stack]))
        self.stacks[end_stack].append(container)
        self.move_sound.play()

