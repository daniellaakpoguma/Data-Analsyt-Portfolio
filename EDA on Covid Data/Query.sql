-- See all available columns from death
SELECT * 
FROM dbo.CovidDeaths;

SELECT *
FROM dbo.CovidVaccinations;


/* Queries for Tableau */
-- Select Data that we are going to be using 
SELECT Location, date, total_cases, new_cases, total_deaths, population
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL;

--------- MY COUNTRY (CANADA) ----------
-- Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in Canada
SELECT location, date, total_cases, total_deaths,
CASE WHEN total_cases = 0 THEN 0 ELSE (total_deaths/total_cases) * 100 END AS DeathPercentage
FROM dbo.CovidDeaths
WHERE location like '%canada%'
AND continent IS NOT NULL
order by 1,2;

-- Total Cases vs Population
-- Shows what percentage of population infected with Covid in Canada
SELECT location, date, total_cases, population, (total_cases/population) * 100 AS CasesPercentage
FROM dbo.CovidDeaths
WHERE location like '%canada%'
AND continent IS NOT NULL
order by 1,2;

--------- BY COUNTRY ----------
-- Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid (ALL countries)
SELECT location, date, total_cases, total_deaths,
CASE WHEN total_cases = 0 THEN 0 ELSE (total_deaths/total_cases) * 100 END AS DeathPercentage
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
order by 1,2;

-- Total Cases vs Population
-- Shows what percentage of population infected with Covid (All countries)
SELECT location, date, total_cases, population, (total_cases/population) * 100 AS CasesPercentage
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
order by 1,2;

-- Countries with Highest Infection Rate compared to Population
SELECT location, population, max(total_cases) AS highest_infection_count, max((total_cases/ population) * 100)  AS CovidPercentage
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY CovidPercentage DESC;

-- Countries with Highest Death Count per Population
SELECT location, population, max(total_deaths) AS HighestDeathCount, max((total_deaths/population)) AS DeathCountPerPopulation
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY DeathCountPerPopulation DESC;

--------- BY CONTINENT ----------
-- Showing contintents with the highest death count per population
SELECT continent, max(total_deaths) AS HighestDeathCount, max((total_deaths/population)) AS DeathCountPerPopulation
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY DeathCountPerPopulation DESC;

-- Showing contintents with the highest death count
SELECT continent, MAX(total_deaths) AS TotalDeathCount
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY  TotalDeathCount DESC;

-- Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid (By Continent)
SELECT continent,date, total_cases, population, 
CASE WHEN total_cases = 0 THEN 0 ELSE (total_deaths/total_cases) * 100 END AS DeathPercentage
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1,2;

-- Total Cases vs Population
-- Shows what percentage of population infected with Covid (All countries)
SELECT continent, date, total_cases, population, (total_cases/population) * 100 AS CasesPercentage
FROM dbo.CovidDeaths
WHERE continent IS NOT NULL
order by 1,2;

--------- GLOBAL NUMBERS ----------
SELECT SUM(new_cases) as total_cases, SUM(cast(new_deaths AS INT)) AS total_deaths, SUM(cast(new_deaths AS INT))/SUM(New_Cases)*100 AS DeathPercentage
FROM PortfolioProject..CovidDeaths
WHERE continent is not null 
ORDER BY 1,2;


-- Total Population vs Vaccinations
-- Shows Percentage of Population that has recieved at least one Covid Vaccine
SELECT dea.continent, 
       dea.location, 
       dea.date, 
       dea.population, 
       COALESCE(vac.new_vaccinations, 0) AS new_vaccinations,
       SUM(CONVERT(BIGINT,COALESCE(vac.new_vaccinations, 0))) OVER (PARTITION BY dea.Location ORDER BY dea.location, dea.Date) AS RollingPeopleVaccinated
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
    ON dea.location = vac.location
    AND dea.date = vac.date
WHERE dea.continent IS NOT NULL 
ORDER BY 2, 3;

-- Using CTE to perform Calculation on Partition By in previous query
With PopvsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(BIGINT,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
)
Select *, (RollingPeopleVaccinated/Population)*100 AS RollingPeopleVaccinatedPercentage
From PopvsVac;



-- Using Temp Table to perform Calculation on Partition By in previous query

DROP Table if exists #PercentPopulationVaccinated
Create Table #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(BIGINT,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
WHERE dea.continent IS NOT NULL

Select *, (RollingPeopleVaccinated/Population)*100
From #PercentPopulationVaccinated;

-- Creating View to store data for later visualizations
Create View PercentPopulationVaccinated as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(int,vac.new_vaccinations)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 



