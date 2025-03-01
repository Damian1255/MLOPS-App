class Functions:
    def __init__(self):
        pass

    def get_column_attributes(self, data, convert_to_object=[], convert_to_int=[], custom_order=[]):
        column_attributes = {}
        data = data.dropna()

        for column in convert_to_object:
            # drop missing values
            data = data.dropna(subset=[column])
            # convert to object
            data[column] = data[column].astype("object")

        for column in convert_to_int:
            # drop missing values
            data = data.dropna(subset=[column])
            # convert to int
            data[column] = data[column].astype("int")

        for column in data.columns:
            if data[column].dtype == "object":
                column_attributes[column] = {
                    "unique": list(data[column].unique()),
                    "type": str(data[column].dtype)
                }
            else:
                column_attributes[column] = {
                    "min": str(data[column].min()),
                    "max": str(data[column].max()),
                    "type": str(data[column].dtype)
                }

        # reorder based on custom_order
        if custom_order:
            column_attributes = {k: column_attributes[k] for k in custom_order
                                 if k in column_attributes}
            
        return column_attributes