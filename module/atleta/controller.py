from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional

from module.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaResumo
from module.atleta.models import AtletaModel
from module.categorias.models import CategoriaModel
from module.centro_treinamento.models import CentroTreinamentoModel
from module.contrib.dependencies import DatabaseDependency
from fastapi_pagination import Page, paginate

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    try:
        # Busca a categoria e o centro de treinamento no banco de dados
        categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
        if not categoria:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria não encontrada.")

        centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
        if not centro_treinamento:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Centro de treinamento não encontrado.")

        # Ajuste na criação do objeto AtletaModel
        atleta_dict = atleta_in.model_dump(exclude={'categoria', 'centro_treinamento'})
        atleta = AtletaModel(**atleta_dict, created_at=datetime.utcnow(), categoria_id=categoria.pk_id, centro_treinamento_id=centro_treinamento.pk_id)

        db_session.add(atleta)
        await db_session.commit()
        await db_session.refresh(atleta)
        
        return AtletaOut(
            nome=atleta.nome,
            cpf=atleta.cpf,
            idade=atleta.idade,
            peso=atleta.peso,
            altura=atleta.altura,
            sexo=atleta.sexo,
            created_at=atleta.created_at,
            id=atleta.id,
            categoria={"nome": categoria.nome},
            centro_treinamento={"nome": centro_treinamento.nome}
        )
    except IntegrityError:
        # Manipula o erro de CPF duplicado, conforme o desafio
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
        )
    except Exception as e:
        # Manipula outros erros
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado: {str(e)}"
        )

@router.get(
    '/',
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaResumo]
)
async def query(
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(None, description="Nome do atleta para filtro"),
    cpf: Optional[str] = Query(None, description="CPF do atleta para filtro")
) -> Page[AtletaResumo]:
    query_stmt = select(AtletaModel)
    
    if nome:
        query_stmt = query_stmt.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query_stmt = query_stmt.filter(AtletaModel.cpf == cpf)

    atletas = (await db_session.execute(query_stmt)).scalars().all()
    
    # Mapeia os objetos do SQLAlchemy para o schema de resumo
    atletas_resumo = [
        AtletaResumo(
            nome=a.nome,
            categoria=a.categoria.nome if a.categoria else None,
            centro_treinamento=a.centro_treinamento.nome if a.centro_treinamento else None
        ) for a in atletas
    ]
    
    return paginate(atletas_resumo)

@router.get(
    '/{id}',
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    return AtletaOut(
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        created_at=atleta.created_at,
        id=atleta.id,
        categoria={"nome": atleta.categoria.nome},
        centro_treinamento={"nome": atleta.centro_treinamento.nome}
    )

@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut(
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        created_at=atleta.created_at,
        id=atleta.id,
        categoria={"nome": atleta.categoria.nome},
        centro_treinamento={"nome": atleta.centro_treinamento.nome}
    )

@router.delete(
    '/{id}',
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    await db_session.delete(atleta)
    await db_session.commit()