from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    nombre: Mapped[str] = mapped_column(String(120))
    apellido: Mapped[str] = mapped_column(String(120))
    fecha_suscripcion: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    favoritos_personajes = relationship("PersonajeFav", back_populates="usuario", cascade="all, delete")
    favoritos_planetas = relationship("PlanetaFav", back_populates="usuario", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_suscripcion": self.fecha_suscripcion.isoformat() if self.fecha_suscripcion else None
        }


class Personaje(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    genero: Mapped[str] = mapped_column(String(50))
    año_nacimiento: Mapped[str] = mapped_column(String(50))
    altura: Mapped[int] = mapped_column()
    peso: Mapped[int] = mapped_column()
    color_piel: Mapped[str] = mapped_column(String(50))

    favoritos = relationship("PersonajeFav", back_populates="personaje", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "año_nacimiento": self.año_nacimiento,
            "altura": self.altura,
            "peso": self.peso,
            "color_piel": self.color_piel
        }


class Planeta(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    clima: Mapped[str] = mapped_column(String(100))
    terreno: Mapped[str] = mapped_column(String(100))
    poblacion: Mapped[int] = mapped_column(BigInteger)
    diametro: Mapped[int] = mapped_column()

    favoritos = relationship("PlanetaFav", back_populates="planeta", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion,
            "diametro": self.diametro
        }


class PersonajeFav(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    personaje_id: Mapped[int] = mapped_column(ForeignKey("personaje.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="favoritos_personajes")
    personaje = relationship("Personaje", back_populates="favoritos")


class PlanetaFav(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), nullable=False)
    planeta_id: Mapped[int] = mapped_column(ForeignKey("planeta.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="favoritos_planetas")
    planeta = relationship("Planeta", back_populates="favoritos")
