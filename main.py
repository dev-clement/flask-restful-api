from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video is required', required=True)
video_put_args.add_argument('views', type=int, help='Views of the video is required', required=True)
video_put_args.add_argument('likes', type=int, help='Likes of the video is required', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='Name of the video is required')
video_update_args.add_argument('views', type=int, help='Views of the video is required')
video_update_args.add_argument('likes', type=int, help='Likes of the video is required')

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'''Video(name={self.name}, views={self.views}, likes={self.likes})'''

with app.app_context():
    db.create_all()

resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_field)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(http_status_code=404, message='Could not find the given video...')
        return result

    @marshal_with(resource_field)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(http_status_code=409, message='A video has already this identifier...')
        video = VideoModel(id=video_id, name=args['name'], likes=args['likes'], views=args['views'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        query = VideoModel.query.filter_by(id=video_id).first()
        if not query:
            abort(http_status_code=404, message='The video doesnt exist, cannot update...')
        if args['name']:
            query.name = args['name']
        if args['views']:
            query.views = args['views']
        if args['likes']:
            query.likes = args['likes']
        db.session.commit()
        return query
        
    
    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)