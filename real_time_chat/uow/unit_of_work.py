from sqlalchemy.orm import Session


class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory


    def __enter__(self):
        self.session: Session = self.session_factory()
        return self


    def __exit__(self, *args):
        self.session.close()


    def commit(self):
        self.session.commit()
