from app.services.db.db_models import User
import uuid


class DBCommands:

    async def get_or_create_user(self):
        current_user = types.User.get_current()

        if current_user:
            old_user = await User.query.where(User.id == current_user.id).gino.first()
            if old_user:
                return old_user

            user = User(id=current_user.id, nickname=current_user.username)
            await user.create()
            return user
        else:
            return None

    async def get_all_users(self):
        return await User.query.gino.all()

    async def update_user(self, **kwargs):
        user = await self.get_or_create_user()
        return await User.update.values(**kwargs).where(User.id == user.id).gino.status()

    async def is_price_list_exists(self, name):
        price_list = await PriceList.query.where(PriceList.name == name).gino.first()

        if price_list:
            return True
        return False

    async def delete_price_list(self, price_list_id):
        return await PriceList.delete.where(PriceList.id == price_list_id).gino.status()
