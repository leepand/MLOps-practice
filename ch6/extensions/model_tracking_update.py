import contextlib
from algolink.utils.log import logger
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from mlops.ext.sqlalchemy.models import Base,TExperiment
import time

class Experiment(object):
    def __init__(self, db_uri: str):
        self.db_uri = db_uri
        self._engine = create_engine(db_uri)
        Base.metadata.create_all(self._engine)
        self._Session = sessionmaker(bind=self._engine)
        self._active_session = None
    @contextlib.contextmanager
    def _session(self) -> Session:
        if self._active_session is None:
            logger.debug('Creating session for %s', self.db_uri)
            self._active_session = self._Session()
            new_session = True
        else:
            new_session = False

        try:
            yield self._active_session

            if new_session:
                self._active_session.commit()
        except:  # noqa
            if new_session:
                self._active_session.rollback()
            raise
        finally:
            if new_session:
                self._active_session.close()
                self._active_session = None
    def _create_exp(self,obj):
        with self._session() as s:
            p = obj
            s.add(p)
            try:
                logger.debug('Inserting object %s', p)
                s.commit()
            except IntegrityError:
                raise error_type(obj)
            return obj
