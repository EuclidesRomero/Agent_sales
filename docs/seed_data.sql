-- Datos de prueba para la base de datos - Restaurante de Comida Rápida Colombiano
-- Ejecutar en orden para mantener las relaciones

-- 1. Insertar Business (Negocio)
INSERT INTO businesses (name, description, phone, email, website, address, city, country, created_at, updated_at)
VALUES (
    'Sabor Colombiano Express',
    'Restaurante de comida rápida colombiana especializado en arepas, empanadas, perros calientes y hamburguesas con sabor colombiano. Ofrecemos comida rápida auténtica, fresca y deliciosa con ingredientes de calidad. Servicio rápido para llevar o comer en el lugar.',
    '+1-555-456-7890',
    'pedidos@saborcolombiano.com',
    'https://www.saborcolombianoexpress.com',
    'Carrera 7 #32-15, Zona Gourmet',
    'Bogotá',
    'Colombia',
    NOW(),
    NOW()
);

-- 2. Insertar BusinessHour (Horarios)
-- day_of_week: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday
INSERT INTO business_hours (business_id, day_of_week, open_time, close_time, is_closed, created_at, updated_at)
VALUES 
    (1, 0, '11:00:00', '21:00:00', false, NOW(), NOW()),  -- Domingo
    (1, 1, '10:00:00', '22:00:00', false, NOW(), NOW()),  -- Lunes
    (1, 2, '10:00:00', '22:00:00', false, NOW(), NOW()),  -- Martes
    (1, 3, '10:00:00', '22:00:00', false, NOW(), NOW()),  -- Miércoles
    (1, 4, '10:00:00', '22:00:00', false, NOW(), NOW()),  -- Jueves
    (1, 5, '10:00:00', '23:00:00', false, NOW(), NOW()),  -- Viernes
    (1, 6, '11:00:00', '23:00:00', false, NOW(), NOW()); -- Sábado

-- 3. Insertar Categories (Categorías)
-- Categorías principales
INSERT INTO categories (business_id, name, parent_id, created_at, updated_at)
VALUES 
    (1, 'Arepas', NULL, NOW(), NOW()),
    (1, 'Empanadas', NULL, NOW(), NOW()),
    (1, 'Perros Calientes', NULL, NOW(), NOW()),
    (1, 'Hamburguesas', NULL, NOW(), NOW()),
    (1, 'Bebidas', NULL, NOW(), NOW()),
    (1, 'Postres', NULL, NOW(), NOW()),
    (1, 'Combos', NULL, NOW(), NOW());

-- Subcategorías
INSERT INTO categories (business_id, name, parent_id, created_at, updated_at)
VALUES 
    (1, 'Arepas Rellenas', 1, NOW(), NOW()),
    (1, 'Arepas con Todo', 1, NOW(), NOW()),
    (1, 'Empanadas de Carne', 2, NOW(), NOW()),
    (1, 'Empanadas de Pollo', 2, NOW(), NOW()),
    (1, 'Perros Colombianos', 3, NOW(), NOW()),
    (1, 'Perros Especiales', 3, NOW(), NOW()),
    (1, 'Hamburguesas Colombianas', 4, NOW(), NOW()),
    (1, 'Hamburguesas Clásicas', 4, NOW(), NOW()),
    (1, 'Gaseosas', 5, NOW(), NOW()),
    (1, 'Jugos Naturales', 5, NOW(), NOW()),
    (1, 'Postres Típicos', 6, NOW(), NOW()),
    (1, 'Helados', 6, NOW(), NOW()),
    (1, 'Combos Personales', 7, NOW(), NOW()),
    (1, 'Combos Familiares', 7, NOW(), NOW());

-- 4. Insertar BusinessResources (Productos/Servicios)
INSERT INTO business_resources (business_id, category_id, type, name, description, attributes, active, created_at, updated_at)
VALUES 
    -- Arepas Rellenas
    (1, 8, 'PRODUCT', 'Arepa de Carne Mechada', 'Arepa rellena de carne mechada deshebrada con queso', 
     '{"nivel_picante": "suave", "proteina": "res", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    (1, 8, 'PRODUCT', 'Arepa de Pollo', 'Arepa rellena de pollo desmenuzado con mayonesa y queso', 
     '{"nivel_picante": "suave", "proteina": "pollo", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    (1, 8, 'PRODUCT', 'Arepa de Queso', 'Arepa rellena de queso derretido', 
     '{"nivel_picante": "ninguno", "proteina": "queso", "vegetariano": true}', 
     true, NOW(), NOW()),
    
    -- Arepas con Todo
    (1, 9, 'PRODUCT', 'Arepa con Todo', 'Arepa con carne, pollo, huevo, queso y aguacate', 
     '{"nivel_picante": "medio", "proteina": "mixta", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    (1, 9, 'PRODUCT', 'Arepa Pepitoria', 'Arepa con huevo picado, cebolla y tomate', 
     '{"nivel_picante": "suave", "proteina": "huevo", "vegetariano": true}', 
     true, NOW(), NOW()),
    
    -- Empanadas de Carne
    (1, 10, 'PRODUCT', 'Empanada de Carne', 'Empanada frita de masa de maíz con relleno de carne y papa', 
     '{"nivel_picante": "medio", "proteina": "res", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    (1, 10, 'PRODUCT', 'Empanada de Carne Especial', 'Empanada de carne con queso adicional', 
     '{"nivel_picante": "medio", "proteina": "res", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    -- Empanadas de Pollo
    (1, 11, 'PRODUCT', 'Empanada de Pollo', 'Empanada frita de masa de maíz con relleno de pollo y papa', 
     '{"nivel_picante": "suave", "proteina": "pollo", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    -- Perros Colombianos
    (1, 12, 'PRODUCT', 'Perro Colombiano Clásico', 'Perro caliente con papas ralladas, queso, salsas y piña', 
     '{"nivel_picante": "medio", "proteina": "cerdo", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    (1, 12, 'PRODUCT', 'Perro Colombiano con Todo', 'Perro con papas, queso, huevo, bacon y todas las salsas', 
     '{"nivel_picante": "picante", "proteina": "cerdo", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    -- Perros Especiales
    (1, 13, 'PRODUCT', 'Perro Maicito', 'Perro en pan de maíz con carne y salsas especiales', 
     '{"nivel_picante": "medio", "proteina": "cerdo", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    -- Hamburguesas Colombianas
    (1, 14, 'PRODUCT', 'Hamburguesa Colombiana', 'Hamburguesa con carne, queso, huevo, bacon y papas', 
     '{"nivel_picante": "suave", "proteina": "res", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    (1, 14, 'PRODUCT', 'Hamburguesa Llanera', 'Hamburguesa con carne asada, queso llanero y cebolla caramelizada', 
     '{"nivel_picante": "suave", "proteina": "res", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    -- Hamburguesas Clásicas
    (1, 15, 'PRODUCT', 'Hamburguesa Clásica', 'Hamburguesa con carne, lechuga, tomate y queso', 
     '{"nivel_picante": "ninguno", "proteina": "res", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    (1, 15, 'PRODUCT', 'Hamburguesa de Pollo', 'Hamburguesa de pollo con vegetales frescos', 
     '{"nivel_picante": "ninguno", "proteina": "pollo", "vegetariano": false}', 
     true, NOW(), NOW()),
    
    -- Gaseosas
    (1, 16, 'PRODUCT', 'Gaseosa Colombiana', 'Gaseosa tradicional colombiana (variedad)', 
     '{"tamano": "350ml", "alcohol": false, "tipo": "gaseosa"}', 
     true, NOW(), NOW()),
    
    (1, 16, 'PRODUCT', 'Gaseosa Litro', 'Gaseosa en presentación de litro para compartir', 
     '{"tamano": "1L", "alcohol": false, "tipo": "gaseosa"}', 
     true, NOW(), NOW()),
    
    -- Jugos Naturales
    (1, 17, 'PRODUCT', 'Jugo de Lulada', 'Jugo de lulo con limón y azúcar', 
     '{"tamano": "500ml", "alcohol": false, "tipo": "natural"}', 
     true, NOW(), NOW()),
    
    (1, 17, 'PRODUCT', 'Jugo de Maracuyá', 'Jugo natural de maracuyá', 
     '{"tamano": "500ml", "alcohol": false, "tipo": "natural"}', 
     true, NOW(), NOW()),
    
    -- Postres Típicos
    (1, 18, 'PRODUCT', 'Postre de Tres Leches', 'Bizcocho bañado en tres tipos de leche con merengue', 
     '{"nivel_picante": "ninguno", "vegetariano": true}', 
     true, NOW(), NOW()),
    
    (1, 18, 'PRODUCT', 'Bocadillo con Queso', 'Bocadillo de guayaba con queso crema', 
     '{"nivel_picante": "ninguno", "vegetariano": true}', 
     true, NOW(), NOW()),
    
    -- Helados
    (1, 19, 'PRODUCT', 'Helado de Salpicón', 'Helado de frutas tropicales con crema', 
     '{"nivel_picante": "ninguno", "vegetariano": true}', 
     true, NOW(), NOW()),
    
    -- Combos Personales
    (1, 20, 'PACKAGE', 'Combo Personal 1', '1 arepa + 1 empanada + 1 gaseosa', 
     '{"porciones": 1, "incluye": "arepa, empanada, gaseosa"}', 
     true, NOW(), NOW()),
    
    (1, 20, 'PACKAGE', 'Combo Personal 2', '1 perro + 1 papas + 1 gaseosa', 
     '{"porciones": 1, "incluye": "perro, papas, gaseosa"}', 
     true, NOW(), NOW()),
    
    -- Combos Familiares
    (1, 21, 'PACKAGE', 'Combo Familiar', '4 arepas + 4 empanadas + 2 gaseosas litro', 
     '{"porciones": 4, "incluye": "4 arepas, 4 empanadas, 2L gaseosa"}', 
     true, NOW(), NOW()),
    
    (1, 21, 'PACKAGE', 'Combo Fiesta', '6 perros + 2 papas grandes + 2 gaseosas litro', 
     '{"porciones": 6, "incluye": "6 perros, 2 papas grandes, 2L gaseosa"}', 
     true, NOW(), NOW());

-- 5. Insertar BusinessResourceVariants (Variantes de productos)
INSERT INTO business_resource_variants (resource_id, name, price, stock, sku, is_available, is_default, attributes, created_at, updated_at)
VALUES 
    -- Arepa de Carne Mechada variantes
    (1, 'Arepa de Carne Mechada - Individual', 12000.00, NULL, 'AREPA-CARNE-1', true, true, 
     '{"tamano": "regular", "extra_queso": false}', NOW(), NOW()),
    (1, 'Arepa de Carne Mechada - Grande', 15000.00, NULL, 'AREPA-CARNE-G', true, false, 
     '{"tamano": "grande", "extra_queso": false}', NOW(), NOW()),
    (1, 'Arepa de Carne Mechada - Extra Queso', 16000.00, NULL, 'AREPA-CARNE-EQ', true, false, 
     '{"tamano": "regular", "extra_queso": true}', NOW(), NOW()),
    
    -- Arepa de Pollo variantes
    (2, 'Arepa de Pollo - Individual', 11000.00, NULL, 'AREPA-POLLO-1', true, true, 
     '{"tamano": "regular"}', NOW(), NOW()),
    (2, 'Arepa de Pollo - Grande', 14000.00, NULL, 'AREPA-POLLO-G', true, false, 
     '{"tamano": "grande"}', NOW(), NOW()),
    
    -- Arepa de Queso variantes
    (3, 'Arepa de Queso - Individual', 8000.00, NULL, 'AREPA-QUESO-1', true, true, 
     '{"tamano": "regular"}', NOW(), NOW()),
    (3, 'Arepa de Queso - Grande', 10000.00, NULL, 'AREPA-QUESO-G', true, false, 
     '{"tamano": "grande"}', NOW(), NOW()),
    
    -- Arepa con Todo variantes
    (4, 'Arepa con Todo - Regular', 18000.00, NULL, 'AREPA-TODO-1', true, true, 
     '{"tamano": "regular"}', NOW(), NOW()),
    (4, 'Arepa con Todo - Grande', 22000.00, NULL, 'AREPA-TODO-G', true, false, 
     '{"tamano": "grande"}', NOW(), NOW()),
    
    -- Arepa Pepitoria variantes
    (5, 'Arepa Pepitoria - Regular', 10000.00, NULL, 'AREPA-PEPI-1', true, true, 
     '{"tamano": "regular"}', NOW(), NOW()),
    
    -- Empanada de Carne variantes
    (6, 'Empanada de Carne - Unidad', 3500.00, NULL, 'EMP-CARNE-1', true, true, 
     '{"cantidad": 1}', NOW(), NOW()),
    (6, 'Empanada de Carne - 3 Unidades', 10000.00, NULL, 'EMP-CARNE-3', true, false, 
     '{"cantidad": 3}', NOW(), NOW()),
    (6, 'Empanada de Carne - 6 Unidades', 19000.00, NULL, 'EMP-CARNE-6', true, false, 
     '{"cantidad": 6}', NOW(), NOW()),
    
    -- Empanada de Carne Especial variantes
    (7, 'Empanada de Carne Especial - Unidad', 4500.00, NULL, 'EMP-CARNE-ESP-1', true, true, 
     '{"cantidad": 1}', NOW(), NOW()),
    (7, 'Empanada de Carne Especial - 3 Unidades', 13000.00, NULL, 'EMP-CARNE-ESP-3', true, false, 
     '{"cantidad": 3}', NOW(), NOW()),
    
    -- Empanada de Pollo variantes
    (8, 'Empanada de Pollo - Unidad', 3500.00, NULL, 'EMP-POLLO-1', true, true, 
     '{"cantidad": 1}', NOW(), NOW()),
    (8, 'Empanada de Pollo - 3 Unidades', 10000.00, NULL, 'EMP-POLLO-3', true, false, 
     '{"cantidad": 3}', NOW(), NOW()),
    
    -- Perro Colombiano Clásico variantes
    (9, 'Perro Colombiano Clásico - Regular', 14000.00, NULL, 'PERRO-CLAS-1', true, true, 
     '{"tamano": "regular"}', NOW(), NOW()),
    (9, 'Perro Colombiano Clásico - Grande', 17000.00, NULL, 'PERRO-CLAS-G', true, false, 
     '{"tamano": "grande"}', NOW(), NOW()),
    
    -- Perro Colombiano con Todo variantes
    (10, 'Perro Colombiano con Todo - Regular', 18000.00, NULL, 'PERRO-TODO-1', true, true, 
     '{"tamano": "regular"}', NOW(), NOW()),
    (10, 'Perro Colombiano con Todo - Grande', 22000.00, NULL, 'PERRO-TODO-G', true, false, 
     '{"tamano": "grande"}', NOW(), NOW()),
    
    -- Perro Maicito variantes
    (11, 'Perro Maicito - Regular', 15000.00, NULL, 'PERRO-MAIC-1', true, true, 
     '{"tamano": "regular"}', NOW(), NOW()),
    
    -- Hamburguesa Colombiana variantes
    (12, 'Hamburguesa Colombiana - Simple', 22000.00, NULL, 'BURG-COL-1', true, true, 
     '{"carne": 1}', NOW(), NOW()),
    (12, 'Hamburguesa Colombiana - Doble', 28000.00, NULL, 'BURG-COL-2', true, false, 
     '{"carne": 2}', NOW(), NOW()),
    
    -- Hamburguesa Llanera variantes
    (13, 'Hamburguesa Llanera - Simple', 24000.00, NULL, 'BURG-LLAN-1', true, true, 
     '{"carne": 1}', NOW(), NOW()),
    (13, 'Hamburguesa Llanera - Doble', 30000.00, NULL, 'BURG-LLAN-2', true, false, 
     '{"carne": 2}', NOW(), NOW()),
    
    -- Hamburguesa Clásica variantes
    (14, 'Hamburguesa Clásica - Simple', 18000.00, NULL, 'BURG-CLA-1', true, true, 
     '{"carne": 1}', NOW(), NOW()),
    (14, 'Hamburguesa Clásica - Doble', 23000.00, NULL, 'BURG-CLA-2', true, false, 
     '{"carne": 2}', NOW(), NOW()),
    
    -- Hamburguesa de Pollo variantes
    (15, 'Hamburguesa de Pollo - Simple', 17000.00, NULL, 'BURG-POL-1', true, true, 
     '{"carne": 1}', NOW(), NOW()),
    
    -- Gaseosa Colombiana variantes
    (16, 'Gaseosa Colombiana - Personal', 4000.00, NULL, 'GASEOSA-P', true, true, 
     '{"tamano": "350ml"}', NOW(), NOW()),
    (16, 'Gaseosa Colombiana - Litro', 7000.00, NULL, 'GASEOSA-L', true, false, 
     '{"tamano": "1L"}', NOW(), NOW()),
    
    -- Gaseosa Litro variantes
    (17, 'Gaseosa Litro - Regular', 7000.00, NULL, 'GASEOSA-LITRO', true, true, 
     '{"tamano": "1L"}', NOW(), NOW()),
    
    -- Jugo de Lulada variantes
    (18, 'Jugo de Lulada - Personal', 8000.00, NULL, 'JUGO-LULA-P', true, true, 
     '{"tamano": "500ml"}', NOW(), NOW()),
    (18, 'Jugo de Lulada - Litro', 14000.00, NULL, 'JUGO-LULA-L', true, false, 
     '{"tamano": "1L"}', NOW(), NOW()),
    
    -- Jugo de Maracuyá variantes
    (19, 'Jugo de Maracuyá - Personal', 8000.00, NULL, 'JUGO-MARA-P', true, true, 
     '{"tamano": "500ml"}', NOW(), NOW()),
    (19, 'Jugo de Maracuyá - Litro', 14000.00, NULL, 'JUGO-MARA-L', true, false, 
     '{"tamano": "1L"}', NOW(), NOW()),
    
    -- Postre de Tres Leches variantes
    (20, 'Postre de Tres Leches - Porción', 12000.00, NULL, 'POSTRE-TL-1', true, true, 
     '{"tamano": "porcion"}', NOW(), NOW()),
    
    -- Bocadillo con Queso variantes
    (21, 'Bocadillo con Queso - Porción', 9000.00, NULL, 'BOCA-Q-1', true, true, 
     '{"tamano": "porcion"}', NOW(), NOW()),
    
    -- Helado de Salpicón variantes
    (22, 'Helado de Salpicón - Copa', 10000.00, NULL, 'HELA-SALP-1', true, true, 
     '{"tamano": "copa"}', NOW(), NOW()),
    
    -- Combo Personal 1 variantes
    (23, 'Combo Personal 1 - Regular', 25000.00, NULL, 'COMBO-P1', true, true, 
     '{"incluye": "arepa, empanada, gaseosa"}', NOW(), NOW()),
    
    -- Combo Personal 2 variantes
    (24, 'Combo Personal 2 - Regular', 28000.00, NULL, 'COMBO-P2', true, true, 
     '{"incluye": "perro, papas, gaseosa"}', NOW(), NOW()),
    
    -- Combo Familiar variantes
    (25, 'Combo Familiar - Regular', 65000.00, NULL, 'COMBO-FAM', true, true, 
     '{"porciones": 4, "incluye": "4 arepas, 4 empanadas, 2L gaseosa"}', NOW(), NOW()),
    
    -- Combo Fiesta variantes
    (26, 'Combo Fiesta - Regular', 85000.00, NULL, 'COMBO-FIESTA', true, true, 
     '{"porciones": 6, "incluye": "6 perros, 2 papas grandes, 2L gaseosa"}', NOW(), NOW());

-- 6. Insertar KnowledgeDocuments (Base de conocimiento)
INSERT INTO knowledge_documents (business_id, document_type, title, content, created_at, updated_at)
VALUES 
    -- FAQ
    (1, 'FAQ', '¿Cuál es el tiempo de espera para pedidos?', 
     'Para pedidos en el local, el tiempo promedio de preparación es de 10-15 minutos. En horarios pico (12:00-14:00 y 19:00-21:00) puede extenderse a 20 minutos. Para pedidos para llevar, recomendamos llamar con 15 minutos de anticipación. Pedidos grandes (más de 10 items) requieren 30 minutos de preparación.', 
     NOW(), NOW()),
    
    (1, 'FAQ', '¿Tienen opciones vegetarianas?', 
     'Sí, ofrecemos varias opciones vegetarianas incluyendo arepa de queso, arepa pepitoria, empanadas de queso, y hamburguesas vegetarianas bajo solicitud. Nuestros jugos naturales y postres como el bocadillo con queso también son vegetarianos. Pregunte a nuestro personal sobre opciones sin carne.', 
     NOW(), NOW()),
    
    (1, 'FAQ', '¿Cuáles son los métodos de pago aceptados?', 
     'Aceptamos efectivo, tarjetas de crédito/débito (Visa, Mastercard, American Express), transferencias bancarias a través de Nequi/DaviPlata, y pagos móviles. Para pedidos grandes, aceptamos pagos divididos. No hay mínimo de compra para usar tarjeta.', 
     NOW(), NOW()),
    
    (1, 'FAQ', '¿Ofrecen servicio de entrega a domicilio?', 
     'Sí, ofrecemos servicio de entrega a domicilio a través de plataformas como Rappi, Didi Food y iFood. También aceptamos pedidos por teléfono para entrega en zona cercana (radio de 3km). El costo de entrega varía según la distancia y plataforma.', 
     NOW(), NOW()),
    
    (1, 'FAQ', '¿Puedo personalizar mi pedido?', 
     '¡Por supuesto! Puedes personalizar tus arepas, perros y hamburguesas agregando o quitando ingredientes. Extra queso, bacon, huevo, salsas adicionales y más están disponibles. Algunas personalizaciones tienen costo adicional. Pregunta a nuestro personal por las opciones disponibles.', 
     NOW(), NOW()),
    
    -- Políticas
    (1, 'POLICY', 'Política de Devoluciones', 
     'Si hay algún problema con tu pedido, por favor notifícanos inmediatamente. No aceptamos devoluciones de alimentos consumidos, pero reemplazaremos cualquier item que no cumpla con tus expectativas o esté incorrectamente preparado. Para pedidos a domicilio, reporta cualquier problema dentro de 30 minutos de la entrega.', 
     NOW(), NOW()),
    
    (1, 'POLICY', 'Política de Privacidad', 
     'En Sabor Colombiano Express, valoramos tu privacidad. Recopilamos información necesaria para procesar pedidos y mejorar servicios. No compartimos tu información con terceros sin consentimiento. Tus datos están protegidos con medidas de seguridad adecuadas. Puedes solicitar eliminación de datos contactándonos.', 
     NOW(), NOW()),
    
    -- Información del negocio
    (1, 'BUSINESS_INFO', 'Sobre Sabor Colombiano Express', 
     'Sabor Colombiano Express es un restaurante de comida rápida colombiana fundado en 2018. Nos especializamos en arepas, empanadas, perros colombianos y hamburguesas con sabor auténtico. Nuestra misión es llevar el sabor de Colombia a cada platillo, usando recetas tradicionales y ingredientes frescos. Servicio rápido y sabor casero son nuestra marca.', 
     NOW(), NOW()),
    
    (1, 'BUSINESS_INFO', 'Especialidades de la Casa', 
     'Nuestras especialidades incluyen: Arepas rellenas con carne mechada, pollo o queso; Empanadas crujientes de masa de maíz; Perros colombianos con papas ralladas, queso y salsas; Hamburguesas colombianas con queso llanero; y jugos naturales como lulada y maracuyá. Todo preparado al momento con técnicas tradicionales.', 
     NOW(), NOW()),
    
    (1, 'BUSINESS_INFO', 'Servicios para Eventos', 
     'Ofrecemos combos familiares y paquetes para fiestas y reuniones. Nuestros combos familiares incluyen arepas, empanadas y bebidas para compartir. Para eventos grandes, ofrecemos catering con menús personalizados. Contáctanos con al menos 48 horas de anticipación para pedidos grandes.', 
     NOW(), NOW()),
    
    -- Instrucciones de tono
    (1, 'TONE_INSTRUCTIONS', 'Guía de Comunicación', 
     'Mantén un tono amigable, energético y servicial, típico de la calidez colombiana. Usa lenguaje coloquial pero respetuoso. Sé rápido y eficiente en las respuestas. Demuestra entusiasmo por la comida colombiana. Sé empático con cualquier demora o problema. La prioridad es hacer sentir al cliente como en casa, con la calidez característica de nuestra cultura.', 
     NOW(), NOW()),
    
    -- Información de productos
    (1, 'PRODUCT_INFO', 'Arepas - Descripción', 
     'Nuestras arepas están hechas con masa de maíz precocida, asadas a la plancha hasta quedar doradas por fuera y suaves por dentro. Las rellenamos con carne mechada deshebrada, pollo con mayonesa, o queso derretido. Cada arepa se prepara al momento para asegurar la frescura y autenticidad del sabor colombiano.', 
     NOW(), NOW()),
    
    (1, 'PRODUCT_INFO', 'Empanadas - Preparación', 
     'Nuestras empanadas son preparadas con masa de maíz amarillo, rellenas de carne molida con papa o pollo desmenuzado, y fritas hasta quedar doradas y crujientes. Se sirven con nuestra salsa hogao casera. La masa se hace diariamente y el relleno se prepara con especias tradicionales colombianas.', 
     NOW(), NOW()),
    
    (1, 'PRODUCT_INFO', 'Perro Colombiano - Ingredientes', 
     'El perro colombiano clásico incluye salchicha, papas ralladas crujientes, queso mozzarella, salsa rosada, piña en trozos, y salsas adicionales al gusto. Todo servido en pan de perro tostado. Nuestra versión "con todo" agrega huevo, bacon y todas las salsas disponibles. Es una experiencia completa de sabores.', 
     NOW(), NOW()),
    
    (1, 'PRODUCT_INFO', 'Jugos Naturales - Preparación', 
     'Nuestros jugos naturales son preparados con frutas frescas de temporada. La lulada se hace con pulpa de lulo, limón y azúcar al gusto. El jugo de maracuyá es natural sin conservadores. Ambos son preparados al momento y pueden servirse con o sin azúcar. También ofrecemos otras variedades según disponibilidad de frutas.', 
     NOW(), NOW()),
    
    (1, 'PRODUCT_INFO', 'Información Alérgica', 
     'Informamos que nuestra cocina maneja alérgenos comunes incluyendo gluten (en panes y hamburguesas), lácteos (quesos, salsas), huevos, y nueces. Aunque tomamos precauciones, no podemos garantizar ausencia total de trazas. Por favor informa a nuestro personal sobre cualquier alergia. Tenemos opciones sin gluten (arepas) disponibles bajo solicitud.', 
     NOW(), NOW());
