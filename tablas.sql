USE RentACar
GO;

/****** Object:  Table [dbo].[Estados]    Script Date: 10/19/2024 10:37:39 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Estados](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](32) NULL,
 CONSTRAINT [PK_Estados] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Tipos]    Script Date: 10/19/2024 10:37:57 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Tipos](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](32) NULL,
 CONSTRAINT [PK_Tipos] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [dbo].[Combustibles]    Script Date: 10/19/2024 10:38:18 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Combustibles](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](32) NULL,
 CONSTRAINT [PK_Combustibles] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Transmision]    Script Date: 10/19/2024 10:38:33 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Transmision](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](32) NULL,
 CONSTRAINT [PK_Transmision] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Vehiculos]    Script Date: 10/19/2024 10:38:53 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Vehiculos](
	[placa] [varchar](6) NOT NULL,
	[modelo] [varchar](16) NULL,
	[marca] [varchar](32) NULL,
	[anno] [date] NULL,
	[color] [varchar](32) NULL,
	[idTipo] [int] NULL,
	[idCombustible] [int] NULL,
	[idTransmision] [int] NULL,
	[idEstado] [int] NULL,
	[descripcion] [varchar](256) NULL,
 CONSTRAINT [PK_Vehiculos] PRIMARY KEY CLUSTERED 
(
	[placa] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Vehiculos]  WITH CHECK ADD  CONSTRAINT [FK_Vehiculos_Combustibles] FOREIGN KEY([idCombustible])
REFERENCES [dbo].[Combustibles] ([id])
GO

ALTER TABLE [dbo].[Vehiculos] CHECK CONSTRAINT [FK_Vehiculos_Combustibles]
GO

ALTER TABLE [dbo].[Vehiculos]  WITH CHECK ADD  CONSTRAINT [FK_Vehiculos_Estados] FOREIGN KEY([idEstado])
REFERENCES [dbo].[Estados] ([id])
GO

ALTER TABLE [dbo].[Vehiculos] CHECK CONSTRAINT [FK_Vehiculos_Estados]
GO

ALTER TABLE [dbo].[Vehiculos]  WITH CHECK ADD  CONSTRAINT [FK_Vehiculos_Tipos] FOREIGN KEY([idTipo])
REFERENCES [dbo].[Tipos] ([id])
GO

ALTER TABLE [dbo].[Vehiculos] CHECK CONSTRAINT [FK_Vehiculos_Tipos]
GO

ALTER TABLE [dbo].[Vehiculos]  WITH CHECK ADD  CONSTRAINT [FK_Vehiculos_Transmision] FOREIGN KEY([idTransmision])
REFERENCES [dbo].[Transmision] ([id])
GO

ALTER TABLE [dbo].[Vehiculos] CHECK CONSTRAINT [FK_Vehiculos_Transmision]
GO

/****** Object:  Table [dbo].[Riteve]    Script Date: 10/19/2024 10:39:39 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Riteve](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[idVehiculo] [varchar](6) NULL,
	[fecha] [date] NULL,
	[monto] [float] NULL,
	[descripcion] [varchar](64) NULL,
 CONSTRAINT [PK_Riteve] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Riteve]  WITH CHECK ADD  CONSTRAINT [FK_Riteve_Riteve] FOREIGN KEY([idVehiculo])
REFERENCES [dbo].[Vehiculos] ([placa])
GO

ALTER TABLE [dbo].[Riteve] CHECK CONSTRAINT [FK_Riteve_Riteve]
GO

/****** Object:  Table [dbo].[Mantenimientos]    Script Date: 10/19/2024 10:40:27 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Mantenimientos](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[idVehiculo] [varchar](6) NULL,
	[fecha] [datetime] NULL,
	[monto] [float] NULL,
	[descripcion] [varchar](64) NULL,
 CONSTRAINT [PK_Mantenimientos] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Mantenimientos]  WITH CHECK ADD  CONSTRAINT [FK_Mantenimientos_Vehiculos] FOREIGN KEY([idVehiculo])
REFERENCES [dbo].[Vehiculos] ([placa])
GO

ALTER TABLE [dbo].[Mantenimientos] CHECK CONSTRAINT [FK_Mantenimientos_Vehiculos]
GO

/****** Object:  Table [dbo].[Alquileres]    Script Date: 10/19/2024 10:40:40 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Alquileres](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[idVehiculo] [varchar](6) NULL,
	[fechaInicio] [datetime] NULL,
	[fechaFin] [datetime] NULL,
	[cliente] [varchar](64) NULL,
	[monto] [float] NULL,
 CONSTRAINT [PK_Alquileres] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Alquileres]  WITH CHECK ADD  CONSTRAINT [FK_Alquileres_Vehiculos] FOREIGN KEY([idVehiculo])
REFERENCES [dbo].[Vehiculos] ([placa])
GO

ALTER TABLE [dbo].[Alquileres] CHECK CONSTRAINT [FK_Alquileres_Vehiculos]
GO

/****** Object:  Table [dbo].[Accesos]    Script Date: 10/19/2024 10:41:10 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Accesos](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](32) NULL,
 CONSTRAINT [PK_accessos] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Object:  Table [dbo].[Usuarios]    Script Date: 10/19/2024 10:41:24 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Usuarios](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [varchar](64) NULL,
	[contrasena] [varchar](64) NULL,
	[idAcceso] [int] NULL,
 CONSTRAINT [PK_Usuarios] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Usuarios]  WITH CHECK ADD  CONSTRAINT [FK_Usuarios_Accesos] FOREIGN KEY([idAcceso])
REFERENCES [dbo].[Accesos] ([id])
GO

ALTER TABLE [dbo].[Usuarios] CHECK CONSTRAINT [FK_Usuarios_Accesos]
GO