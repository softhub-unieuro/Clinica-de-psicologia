-- Criação da tabela de Usuários
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
        
            -- Campos herdados de AbstractBaseUser e PermissionsMixin
                password VARCHAR(128) NOT NULL,
                    last_login DATETIME NULL,
                        is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                            
                                -- Identificação
                                    matricula VARCHAR(20) NOT NULL UNIQUE,
                                        nome_completo VARCHAR(255) NOT NULL,
                                            cpf VARCHAR(14) NOT NULL UNIQUE,
                                                email VARCHAR(254) NOT NULL UNIQUE,
                                                    telefone VARCHAR(20) NOT NULL,
                                                        data_nascimento DATE NULL,
                                                            foto_perfil VARCHAR(100) NULL,
                                                                cargo VARCHAR(20) NOT NULL,
                                                                    
                                                                        -- Campos Específicos
                                                                            crp VARCHAR(20) NULL,
                                                                                abordagem_teorica VARCHAR(30) NULL,
                                                                                    semestre VARCHAR(20) NULL,
                                                                                        nivel_estagio VARCHAR(10) NULL,
                                                                                            
                                                                                                -- Chaves Estrangeiras (Auto-relacionamento)
                                                                                                    supervisor_vinculado_id INT NULL,
                                                                                                        criado_por_id INT NULL,
                                                                                                            
                                                                                                                -- Auditoria e Status
                                                                                                                    dth_insert DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                                                                                                        dth_delete DATETIME NULL,
                                                                                                                            status_delete BOOLEAN NOT NULL DEFAULT FALSE,
                                                                                                                                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                                                                                                                                    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
                                                                                                                                        
                                                                                                                                            -- Restrições de Chave Estrangeira
                                                                                                                                                FOREIGN KEY (supervisor_vinculado_id) REFERENCES usuario(id) ON DELETE SET NULL,
                                                                                                                                                    FOREIGN KEY (criado_por_id) REFERENCES usuario(id) ON DELETE SET NULL
                                                                                                                                                    );

                                                                                                                                                    -- Criação dos Índices definidos no Meta da classe Usuario
                                                                                                                                                    CREATE INDEX idx_usuario_cargo ON usuario (cargo);
                                                                                                                                                    CREATE INDEX idx_usuario_cpf ON usuario (cpf);
                                                                                                                                                    CREATE INDEX idx_usuario_matricula ON usuario (matricula);
                                                                                                                                                    CREATE INDEX idx_usuario_supervisor ON usuario (supervisor_vinculado_id);
                                                                                                                                                    CREATE INDEX idx_usuario_status ON usuario (status_delete, is_active);