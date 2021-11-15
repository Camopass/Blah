from Engine.Entity import Entity
from Engine.EntityManager import EntityManager
from Engine.Screen import DataScreen


class DebugScreen(DataScreen):
    def get_data(self, entity_manager: EntityManager):
        data = ""
        for entity in entity_manager.entities:
            if type(entity) == Entity:
                data += entity.name + '\n'
                data += "    "
                x = str(entity.x)
                y = str(entity.y)
                data += f'{x if len(x) < 6 else x[:5]}, {y if len(y) < 6 else y[:5]}\n'
                data += "    "
                xvel = str(entity.xvel)
                yvel = str(entity.yvel)
                data += f'{xvel if len(xvel) < 6 else xvel[:5]}, {yvel if len(yvel) < 6 else yvel[:6]}\n'
                data += "    "
                data += str(entity.x_offset) + ', '
                data += str(entity.y_offset) + '\n'

        return data
