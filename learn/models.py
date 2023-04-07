from learn import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(length=30), unique=True, nullable=False)
	password_hash = db.Column(db.String(length=60), nullable=False)
	budget = db.Column(db.Integer(), nullable=False, default=100)

	items = db.relationship('Item', backref='owned_user', lazy=True)

	@property
	def pretty(self):
		neg = self.budget < 0
		v = -1 * self.budget if neg else self.budget
		bud = str(v)
		s = ""
		t = 0
		l = len(bud)
		while True:
			if l>t+3:
				s = ","+bud[-t-3:-t if t else None]+s
			else:
				s = bud[:-t if t else None]+s
				break
			t+=3

		return ("-" if neg else "") + s+'$'

	@property
	def password(self):
		return self.password

	@password.setter
	def password(self, plain_text_password):
		self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

	def check_password_correction(self, attempted_password):
		return bcrypt.check_password_hash(self.password_hash, attempted_password)

	def can_purchase(self, item_obj):
		return item_obj.owner == None and self.budget >= item_obj.price

	def can_sell(self, item_obj):
		return item_obj.owner == self.id
		# return item_obj in self.items


class Item(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(length=30), nullable=False, unique=True)
	price = db.Column(db.Integer, nullable=False)
	barcode = db.Column(db.String(length=12), nullable=False, unique=True)
	description = db.Column(db.String(length=1024), nullable=False)
	owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

	def __repr__(self):
		return f'Item {self.name} owned by {self.owner}'

	def purchase(self, user):
		self.owner = user.id
		user.budget -= self.price
		db.session.commit()

	def sell(self, user):
		self.owner = None
		user.budget += self.price
		db.session.commit()