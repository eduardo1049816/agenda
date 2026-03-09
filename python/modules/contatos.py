from modules.mysql import MySQL

class Contatos:
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        
    def cadastrar(self, db: MySQL):
        query = """
            INSERT INTO contatos (
              nome, email, telefone
            ) VALUES (
                %s, %s, %s
            )
        """
        
        values = (
            self.nome,
            self.email,
            self.telefone
        )
            
        return db.execute_query(query, values)
    
    @staticmethod
    def listar(db: MySQL):
        query = """
            SELECT id,
                    nome,
                    email,
                    telefone
            FROM 
                    contatos
        """
        return db.execute_query(query)
    
    @staticmethod
    def excluir(id_contato, db: MySQL):
        query = "DELETE FROM contatos WHERE id = %s"
        return db.execute_query(query, (id_contato,))

    @staticmethod
    def editar(id_contato, nome, email, telefone, db: MySQL):
        query = """
            UPDATE contatos 
            SET nome = %s, email = %s, telefone = %s 
            WHERE id = %s
        """
        values = (nome, email, telefone, id_contato)
        return db.execute_query(query, values)