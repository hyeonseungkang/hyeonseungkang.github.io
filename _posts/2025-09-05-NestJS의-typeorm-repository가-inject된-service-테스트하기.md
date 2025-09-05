---
layout: post
title:  "NestJS의 Typeorm repository가 inject된 service 테스트하기"
date:   2025-09-05 17:04:00 +0900
---

![NestJS에서_Typeorm_repository_injected_service_테스트하기.jpg](../attachments/images/2025-09-05/NestJS에서_Typeorm_repository_injected_service_테스트하기.jpg)

프로젝트에서 DB를 사용하기 위해 TypeOrmModule을 사용하고 있다.
Service 클래스나 커스텀 repository에서 Typeorm의 repository를 inject한 경우, 테스트코드 작성 요령을 공유한다.

```typescript
describe('CustomRepository', () => {
    let customRepository: CustomRepository;
    // Repository의 전체 메소드를 구현하지 않도록 Pick으로 선택한다. 여기서는 save만를 구현한다.
    const repositoryMock: jest.Mocked<Pick<Repository<EntityName>, 'save'>> =
        {
            save: jest.fn(),
        };
    // save의 동작은 jest.fn 이 반환한 jest.Mock의 mockImplementation 을 통해 구현할 수 있다.
    repositoryMock.save.mockImplementation(
        // mockImplementation 으로 구현할 때 기존 메소드의 type을 지켜야 한다. 여기서는 cast 하였다.
        async (entity: DeepPartial<EntityName>) => {
            // todo
            return entity as DeepPartial<EntityName> & EntityName;
        },
    );

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            providers: [
                CustomRepository,
                // module 내에 dependency가 없는 문제 해결
                {
                    provide: getRepositoryToken(EntityName),
                    useValue: RepositoryMock,
                },
            ],
        }).compile();
        customRepository = module.get<CustomRepository>(CustomRepository);
    });

    it('should be defined', async () => {
        await customRepository.save({
            key: 'value'
        });
    });
});
```
