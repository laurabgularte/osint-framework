import httpx
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO
from modules.base import BaseModule
from osint_engine.models import ModuleResult

class ExifMetadataParser(BaseModule):
    name = "EXIF Metadata Extractor"
    category = "metadata"
    description = "Extrai metadados EXIF de uma URL de imagem."

    async def run(self, target: str) -> ModuleResult:
        if not (target.startswith("http://") or target.startswith("https://")):
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="NOT_FOUND",
                details="O alvo deve ser um URL direto para uma imagem."
            )

        try:
            response = await self.client.get(target)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                exif_data = image._getexif()
                if not exif_data:
                    return ModuleResult(
                        module_name=self.name,
                        category=self.category,
                        target=target,
                        status="NOT_FOUND",
                        details="Sem metadados EXIF encontrados."
                    )

                extracted = {TAGS.get(tag, tag): str(val) for tag, val in exif_data.items() if tag in TAGS}
                return ModuleResult(
                    module_name=self.name,
                    category=self.category,
                    target=target,
                    status="FOUND",
                    details=f"Tags encontradas: {len(extracted)}",
                    raw_data=extracted
                )
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="ERROR",
                details=f"Status HTTP {response.status_code}"
            )
        except Exception as e:
            return ModuleResult(
                module_name=self.name,
                category=self.category,
                target=target,
                status="ERROR",
                details=str(e)
            )