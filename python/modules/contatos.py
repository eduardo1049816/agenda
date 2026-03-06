from modules.mysql import MySQL

class Contatos:
    def __init__(self, nome, email, telefone,):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        
    def cadastrar(self, db: MySQL):
        query = """
            INSERT INTO contatos (
              nome, email, telefone
            ) VALUES (
                %s,%s,%s
            )
        """
        
        values =(
            self.nome,
            self.email,
            self.telefone
        )
            
        return db.execute_query(query, values)
    
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
    
    def editar(self):
        pass
    
    def transferir(self):
        pass